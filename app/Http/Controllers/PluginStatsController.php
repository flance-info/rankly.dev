<?php

namespace App\Http\Controllers;

use Illuminate\Http\Client\RequestException;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;
use Illuminate\Http\Request;

class PluginStatsController extends Controller {
    /**
     * Fetch and return plugin download stats as JSON.
     *
     * @param \Illuminate\Http\Request $request
     * @param string                   $slug
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function download( Request $request, $slug ) {
        $trend    = (int) $request->input( 'trend', 90 ); // Default to 90 days
       
        $cacheKey = "plugin_stats_{$slug}_{$trend}";
        $apiUrl   = "https://api.wordpress.org/stats/plugin/1.0/downloads.php";
        $this->clearCache($slug);
        try {
            $data = Cache::remember( $cacheKey, now()->addHours( 8 ), function () use ( $apiUrl, $slug ) {
                $response = Http::get( $apiUrl, [
                    'slug' => $slug,
                ] );
                if ( $response->successful() ) {
                    return $response->json();
                }
                throw new \Exception( 'Failed to fetch plugin stats.' );
            } );
            // Filter current trend data
            $filteredData = array_slice( $data, - $trend, $trend, true );
            // Get previous trend data
            $previousTrendData = array_slice( $data, - 2 * $trend, $trend, true );
            // Calculate total downloads and percentage change over the trend period
            $totalDownloads         = array_sum( $filteredData );
            $previousTotalDownloads = array_sum( $previousTrendData );
            $firstDay               = reset( $filteredData );
            $lastDay                = end( $filteredData );
            $percentageChange       = $previousTotalDownloads >= 0
                ? ( ( $totalDownloads - $previousTotalDownloads ) / $previousTotalDownloads ) * 100
                : 0;

            return response()->json( [
                'success'          => true,
                'data'             => $filteredData,
                'summary'          => [
                    'total_downloads'   => $totalDownloads,
                   'percentage_change' => round($percentageChange, 0),
                    'start_day'         => $firstDay,
                    'end_day'           => $lastDay,
                ],
                'previous_summary' => [
                    'total_downloads' => $previousTotalDownloads,
                ],
            ] );
        } catch ( RequestException $e ) {
            return response()->json( [
                'success' => false,
                'message' => 'An error occurred while fetching plugin stats: ' . $e->getMessage(),
            ], 500 );
        } catch ( \Exception $e ) {
            return response()->json( [
                'success' => false,
                'message' => $e->getMessage(),
            ], 500 );
        }
    }

    public function clearCache($slug)
    {
        $cacheKey = "plugin_stats_{$slug}_90";  // Match the key format from your download method
        Cache::forget($cacheKey);
        
        // Clear other trend periods too
        Cache::forget("plugin_stats_{$slug}_7");
        Cache::forget("plugin_stats_{$slug}_8");
        Cache::forget("plugin_stats_{$slug}_30");
        Cache::forget("plugin_stats_{$slug}_365");
        
        return response()->json([
            'success' => true,
            'message' => 'Cache cleared successfully'
        ]);
    }
}
