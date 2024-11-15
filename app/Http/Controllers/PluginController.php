<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Models\Plugin;

// Assuming you have a Plugin model
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Session;

class PluginController extends Controller {
    public function searchPlugin( Request $request ) {
        $slug = $request->input( 'slug' );
        $slug = $this->getSlugFromUrl($slug);

        if ( ! $slug ) {
            return response()->json( [ 'error' => 'No plugin slug or url provided' ], 400 );
        }
        if ( ! Auth::check() ) {
            return response()->json( [ 'error' => 'User not authenticated' ], 401 );
        }

        $userId = Auth::id();

        // Check if the plugin already exists for this user
        $existingPlugin = Plugin::where( 'slug', $slug )->where( 'user_id', $userId )->first();
        if ( $existingPlugin ) {
            return response()->json( [ 'message' => 'Plugin already added', 'plugin' => $existingPlugin ], 200 );
        }

        // Query the WordPress.org API
        $response   = Http::get( 'https://api.wordpress.org/plugins/info/1.2/', [
            'action'                       => 'plugin_information',
            'request[slug]'                => $slug,
            'request[fields][description]' => true
        ] );

        // Log the JSON response
        Log::info('WordPress API Response:', $response->json());

        $pluginData = $response->json();
        if ( $pluginData && ! isset( $pluginData['error'] ) ) {
            // Save the plugin data to the session
            Session::put('plugin_data', $pluginData);

            return response()->json([ 'message' => 'Plugin Added to your account', 'plugin' =>  $pluginData ], 201 );
        }

        return response()->json( [ 'error' => 'Plugin not found' ], 404 );
    }

    private function getSlugFromUrl($input) {
        if (filter_var($input, FILTER_VALIDATE_URL)) {
            $path = parse_url($input, PHP_URL_PATH);
            $path = trim($path, '/');
            $segments = explode('/', $path);
            return end($segments);
        }
        return $input;
    }

    public function getSessionPlugins(Request $request) {
        // Retrieve the current session data
        $currentPlugins = Session::get('plugin_data', []);

        // Get the new plugins from the request
        $newPlugins = $request->input('plugins', []);

        // Merge the current session data with the new plugins
        $updatedPlugins = array_merge($currentPlugins, $newPlugins);

        // Update the session with the merged plugins list
        Session::put('plugin_data', $updatedPlugins);

        return response()->json(['message' => 'Session plugins updated successfully', 'plugin_data' => $updatedPlugins]);
    }
}
