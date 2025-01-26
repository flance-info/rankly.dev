<?php

namespace App\Http\Controllers;

use App\Models\Plugin;
use App\Models\PluginKeywordStat;
use Illuminate\Http\Request;
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;

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

            // Get latest stats for each keyword
            $latestStats = DB::table('plugin_keyword_stats as pks1')
                ->select(
                    'pks1.keyword_slug as keyword',
                    'pks1.rank_order',
                    'pks1.stat_date as latest_date',
                    DB::raw('\'en\' as language'),
                    DB::raw('COUNT(*) as occurrences')
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
            $response = collect($keywords)->map(function ($keyword) use ($latestStats, $previousStats) {
                $currentStat = $latestStats->get($keyword);
                $previousStat = $previousStats->get($keyword);

                return [
                    'keyword' => $keyword,
                    'current_position' => $currentStat ? $currentStat->rank_order : 0,
                    'position_change' => $currentStat && $previousStat 
                        ? $previousStat->rank_order - $currentStat->rank_order 
                        : 0,
                    'occurrences' => $currentStat ? $currentStat->occurrences : 0,
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
} 