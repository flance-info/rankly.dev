<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Models\Plugin;

// Assuming you have a Plugin model
use Illuminate\Support\Facades\Auth;

class PluginController extends Controller {
    public function searchPlugin( Request $request ) {
        $slug = $request->input( 'slug' );
        if ( ! $slug ) {
            return response()->json( [ 'error' => 'No plugin slug provided' ], 400 );
        }
        if ( Auth::check() ) {
            $savedata['user_id'] = Auth::id();
        } else {
            return response()->json( [ 'error' => 'User not authenticated' ], 401 );
        }
        // Query the WordPress.org API
        $response   = Http::get( 'https://api.wordpress.org/plugins/info/1.2/', [
            'action'                       => 'plugin_information',
            'request[slug]'                => $slug,
            'request[fields][description]' => true
        ] );
        $pluginData = $response->json();
        if ( $pluginData && ! isset( $pluginData['error'] ) ) {
            // Save the plugin data to the database
            $savedata = [
                'name'    => $pluginData['name'],
                'slug'    => $slug,
                'description' => $pluginData['description'],
                'user_id' => Auth::id(),
            ];
            $plugin = Plugin::create( $savedata );

            return response()->json( $plugin, 201 );
        }

        return response()->json( [ 'error' => 'Plugin not found' ], 404 );
    }
}

