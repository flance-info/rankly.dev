<?php

namespace App\Http\Controllers;

use Illuminate\Http\Client\RequestException;
use Illuminate\Support\Facades\Http;
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
        $apiUrl = "https://api.wordpress.org/stats/plugin/1.0/downloads.php";
        try {
            $response = Http::get( $apiUrl, [
                'slug' => $slug,
            ] );
            if ( $response->successful() ) {
                $data = $response->json();

                return response()->json( [
                    'success' => true,
                    'data'    => $data,
                ] );
            } else {
                return response()->json( [
                    'success' => false,
                    'message' => 'Failed to fetch plugin stats. Please try again later.',
                ], 400 );
            }
        } catch ( RequestException $e ) {
            return response()->json( [
                'success' => false,
                'message' => 'An error occurred while fetching plugin stats: ' . $e->getMessage(),
            ], 500 );
        }
    }
}

