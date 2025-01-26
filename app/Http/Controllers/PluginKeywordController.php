<?php

namespace App\Http\Controllers;

use App\Models\Plugin;
use App\Models\PluginKeywordStat;
use App\Models\UserKeyword;
use Illuminate\Http\Request;
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

class PluginKeywordController extends Controller
{
    public function getKeywords(Request $request)
    {
        try {
            // Validate request parameters
            $request->validate([
                'slug' => 'required|string',
                'keywords' => 'required|array',
                'trend' => 'required|in:7,30,90,365'
            ]);

            $slug = $request->input('slug');
            $keywords = $request->input('keywords');
            $trendDays = (int) $request->input('trend');
            $startDate = Carbon::now()->subDays($trendDays);

            // Get user's tracked keywords
            $userKeywords = UserKeyword::where('user_id', auth()->id())
                ->where('plugin_slug', $slug)
                ->pluck('keyword_slug')
                ->toArray();

            // Find keywords that aren't tracked yet
            $newKeywords = array_diff($keywords, $userKeywords);

            // If there are new keywords, add them for the user
            if (!empty($newKeywords)) {
                $keywordsToAdd = collect($newKeywords)->map(function($keyword) use ($slug) {
                    return [
                        'user_id' => auth()->id(),
                        'plugin_slug' => $slug,
                        'keyword_slug' => $keyword,
                        'status' => 'published',
                        'created_at' => now(),
                        'updated_at' => now()
                    ];
                })->toArray();

                UserKeyword::insert($keywordsToAdd);
                
                // Update userKeywords array with newly added keywords
                $userKeywords = array_merge($userKeywords, $newKeywords);
            }
            $keywords = UserKeyword::where('user_id', auth()->id())
                ->where('plugin_slug', $slug)
                ->where('status', 'published')
                ->pluck('keyword_slug')
                ->toArray();
            // Get readme content from WordPress.org API
            $readmeUrl = "https://plugins.svn.wordpress.org/{$slug}/trunk/readme.txt";
            $response = Http::get($readmeUrl);
            
            // Get plugin description as fallback
            $plugin = Plugin::where('slug', $slug)
                ->select('plugin_data->description as description')
                ->first();

            // Use readme content if available, otherwise use description
            $content = $response->successful() 
                ? strtolower($response->body()) 
                : strtolower($plugin->description ?? '');

            // Remove all URLs
           // $textWithoutUrls = preg_replace('/https?:\/\/\S+/', '', $content);
           // $textWithoutUrls = preg_replace('/www\.\S+/', '', $textWithoutUrls);
           $textWithoutUrls = $content;
            // Count keyword occurrences in cleaned content
            $keywordOccurrences = collect($keywords)->mapWithKeys(function ($keyword) use ($textWithoutUrls) {
                // Count occurrences with word boundaries
                $pattern = '/\b' . preg_quote(strtolower($keyword), '/') . '\b/';
                preg_match_all($pattern, $textWithoutUrls, $matches);
                return [$keyword => count($matches[0])];
            });

            // Get latest stats for each keyword
            $latestStats = DB::table('plugin_keyword_stats as pks1')
                ->select(
                    'pks1.keyword_slug as keyword',
                    'pks1.rank_order',
                    'pks1.stat_date as latest_date',
                    DB::raw('\'en\' as language')
                )
                ->joinSub(
                    DB::table('plugin_keyword_stats')
                        ->select('keyword_slug', DB::raw('MAX(stat_date) as max_date'))
                        ->where('plugin_slug', $slug)
                        ->whereIn('keyword_slug', $keywords)
                        ->groupBy('keyword_slug'),
                    'pks2',
                    function($join) {
                        $join->on('pks1.keyword_slug', '=', 'pks2.keyword_slug')
                             ->on('pks1.stat_date', '=', 'pks2.max_date');
                    }
                )
                ->where('pks1.plugin_slug', $slug)
                ->whereIn('pks1.keyword_slug', $keywords)
                ->groupBy('pks1.keyword_slug', 'pks1.rank_order', 'pks1.stat_date')
                ->get()
                ->keyBy('keyword');

            // Get previous stats for position change calculation
            $previousStats = collect($keywords)->mapWithKeys(function ($keyword) use ($slug, $latestStats) {
                $latestDate = $latestStats->get($keyword)?->latest_date;
                
                if (!$latestDate) {
                    return [$keyword => null];
                }

                return [$keyword => DB::table('plugin_keyword_stats')
                    ->where('plugin_slug', $slug)
                    ->where('keyword_slug', $keyword)
                    ->where('stat_date', '<', $latestDate)
                    ->orderBy('stat_date', 'desc')
                    ->first()
                ];
            });

            // Create response including all keywords
            $response = collect($keywords)->map(function ($keyword) use ($latestStats, $previousStats, $keywordOccurrences) {
                $currentStat = $latestStats->get($keyword);
                $previousStat = $previousStats->get($keyword);

                return [
                    'keyword' => $keyword,
                    'current_position' => $currentStat ? $currentStat->rank_order : 0,
                    'position_change' => $currentStat && $previousStat 
                        ? $previousStat->rank_order - $currentStat->rank_order 
                        : 0,
                    'occurrences' => $keywordOccurrences[$keyword] ?? 0,
                    'language' => 'en',
                    'updated_at' => $currentStat ? $currentStat->latest_date : null
                ];
            });

            return response()->json([
                'success' => true,
                'data' => $response->values()
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error fetching keyword data: ' . $e->getMessage()
            ], 500);
        }
    }

    public function deleteKeywords(Request $request)
    {
        $request->validate([
            'slug' => 'required|string',
            'keywords' => 'required|array'
        ]);

        try {
            UserKeyword::where('user_id', auth()->id())
                ->where('plugin_slug', $request->slug)
                ->whereIn('keyword_slug', $request->keywords)
                ->update(['status' => 'removed']);

            return response()->json([
                'success' => true,
                'message' => 'Keywords removed from tracking successfully'
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error removing keywords: ' . $e->getMessage()
            ], 500);
        }
    }

    public function addKeywords(Request $request)
    {
        $request->validate([
            'slug' => 'required|string',
            'keywords' => 'required|array',
            'keywords.*' => 'required|string'
        ]);

        try {
            $userId = auth()->id();
            $pluginSlug = $request->slug;
            
            foreach($request->keywords as $keyword) {
                UserKeyword::updateOrCreate(
                    [
                        'user_id' => $userId,
                        'plugin_slug' => $pluginSlug,
                        'keyword_slug' => $keyword,
                    ],
                    [
                        'status' => 'published',
                        'updated_at' => now()
                    ]
                );
            }

            return response()->json([
                'success' => true,
                'message' => 'Keywords added successfully'
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error adding keywords: ' . $e->getMessage()
            ], 500);
        }
    }
} 