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

            // Get the latest date for the plugin's keyword stats
            $latestDate = PluginKeywordStat::where('plugin_slug', $slug)
                ->max('stat_date');

            // Get stats for the latest date
            $keywordStats = PluginKeywordStat::where('plugin_slug', $slug)
                ->whereIn('keyword_slug', $keywords)
                ->where('stat_date', $latestDate)
                ->select(
                    'keyword_slug as keyword',
                    DB::raw('\'en\' as language'),
                    'rank_order',
                    DB::raw('COUNT(*) as occurrences')
                )
                ->groupBy('keyword_slug', 'rank_order')
                ->get()
                ->keyBy('keyword');

            // Get previous date stats for position change calculation
            $previousDate = PluginKeywordStat::where('plugin_slug', $slug)
                ->where('stat_date', '<', $latestDate)
                ->max('stat_date');

            $previousStats = PluginKeywordStat::where('plugin_slug', $slug)
                ->whereIn('keyword_slug', $keywords)
                ->where('stat_date', $previousDate)
                ->select('keyword_slug as keyword', 'rank_order')
                ->get()
                ->keyBy('keyword');

            // Create response including all keywords
            $response = collect($keywords)->map(function ($keyword) use ($keywordStats, $previousStats, $latestDate) {
                $currentStat = $keywordStats->get($keyword);
                $previousStat = $previousStats->get($keyword);

                return [
                    'keyword' => $keyword,
                    'current_position' => $currentStat ? $currentStat->rank_order : 0,
                    'position_change' => $currentStat && $previousStat 
                        ? $previousStat->rank_order - $currentStat->rank_order 
                        : 0,
                    'occurrences' => $currentStat ? $currentStat->occurrences : 0,
                    'language' => 'en',
                    'updated_at' => $latestDate // Using latest stat_date for all records
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