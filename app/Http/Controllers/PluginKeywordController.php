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
                'keywords' => 'array',
                'trend' => 'required|in:7,30,90,365'
            ]);

            $slug = $request->input('slug');
            $keywords = $request->input('keywords');
            $trendDays = (int) $request->input('trend');
            $startDate = Carbon::now()->subDays($trendDays);

            // Fetch and update user keywords
            $this->updateUserKeywords($slug);

            // Fetch user's published keywords
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

            // Get plugin ID from slug
            $pluginId = DB::table('plugins')->where('slug', $slug)->value('id');
            if (!$pluginId) {
                return response()->json(['success' => false, 'message' => 'Plugin not found'], 404);
            }

            // Get keyword IDs and create a mapping of slug to ID
            $keywordData = DB::table('keywords')
                ->whereIn('slug', $keywords)
                ->select('id', 'slug')
                ->get();

            $keywordIds = $keywordData->pluck('id')->toArray();
            $keywordSlugToId = $keywordData->pluck('id', 'slug')->toArray();
            $keywordIdToSlug = $keywordData->pluck('slug', 'id')->toArray();

            // Get latest stats for each keyword
            $latestStats = DB::table('plugin_keyword_stats as pks1')
                ->select(
                    'k.slug as keyword',  // Get the slug from keywords table
                    'pks1.rank_order',
                    'pks1.stat_date as latest_date',
                    DB::raw('\'en\' as language')
                )
                ->join('keywords as k', 'pks1.keyword_id', '=', 'k.id')  // Join with keywords table
                ->joinSub(
                    DB::table('plugin_keyword_stats')
                        ->select('keyword_id', DB::raw('MAX(stat_date) as max_date'))  // Use keyword_id
                        ->where('plugin_id', $pluginId)  // Use plugin_id
                        ->whereIn('keyword_id', $keywordIds)  // Use keyword_ids array
                        ->groupBy('keyword_id'),
                    'pks2',
                    function($join) {
                        $join->on('pks1.keyword_id', '=', 'pks2.keyword_id')  // Use keyword_id
                             ->on('pks1.stat_date', '=', 'pks2.max_date');
                    }
                )
                ->where('pks1.plugin_id', $pluginId)  // Use plugin_id
                ->whereIn('pks1.keyword_id', $keywordIds)  // Use keyword_ids array
                ->groupBy('k.slug', 'pks1.rank_order', 'pks1.stat_date')  // Group by slug from keywords table
                ->get()
                ->keyBy('keyword');

            // Get previous stats for position change calculation
            $previousStats = collect($keywords)->mapWithKeys(function ($keyword) use ($slug, $latestStats, $pluginId, $keywordSlugToId) {
                $latestDate = $latestStats->get($keyword)?->latest_date;
                $keywordId = $keywordSlugToId[$keyword] ?? null;
                
                if (!$latestDate || !$keywordId) {
                    return [$keyword => null];
                }

                return [$keyword => DB::table('plugin_keyword_stats')
                    ->where('plugin_id', $pluginId)  // Use plugin_id
                    ->where('keyword_id', $keywordId)  // Use keyword_id
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

    private function updateUserKeywords($slug)
    {
        // Fetch plugin keywords from the plugin data
        $plugin = Plugin::where('slug', $slug)->first();
        $pluginKeywords = $plugin ? $plugin->plugin_data['tags'] ?? [] : [];

        // Fetch user's existing keywords
        $userKeywords = UserKeyword::where('user_id', auth()->id())
            ->where('plugin_slug', $slug)
            ->pluck('keyword_slug')
            ->toArray();

        // Find new keywords that are not yet tracked by the user
        $newKeywords = array_diff($pluginKeywords, $userKeywords);

        // Insert new keywords into user_keywords table
        foreach ($newKeywords as $keyword) {
            UserKeyword::create([
                'user_id' => auth()->id(),
                'plugin_slug' => $slug,
                'keyword_slug' => $keyword,
                'status' => 'published',
                'created_at' => now(),
                'updated_at' => now()
            ]);
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

    public function getUserKeywords($slug)
    {
        try {

            $this->updateUserKeywords($slug);
            $keywords = UserKeyword::where('user_id', auth()->id())
                ->where('plugin_slug', $slug)
                ->where('status', 'published')
                ->pluck('keyword_slug')
                ->toArray();

            return response()->json([
                'success' => true,
                'keywords' => $keywords
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error fetching user keywords: ' . $e->getMessage()
            ], 500);
        }
    }
} 