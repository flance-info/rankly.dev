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
        $cacheKey = "plugin_stats_{$slug}";
        $apiUrl   = "https://api.wordpress.org/stats/plugin/1.0/downloads.php";
        try {
            $data = Cache::remember( $cacheKey, now()->addHours( 5 ), function () use ( $apiUrl, $slug ) {
                $response = Http::get( $apiUrl, [
                    'slug' => $slug,
                ] );


                if ( $response->successful() ) {
                    return $response->json();
                }
                throw new \Exception( 'Failed to fetch plugin stats.' );
            } );

            return response()->json( [
                'success' => true,
                'data'    => $data,
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
}
