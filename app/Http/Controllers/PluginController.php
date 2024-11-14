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
        $pluginData = $response->json();
        if ( $pluginData && ! isset( $pluginData['error'] ) ) {
            // Save the plugin data to the database
            $savedata = [
                'name'    => $pluginData['name'],
                'slug'    => $slug,
                'description' => $pluginData['description'],
                'user_id' => $userId,
            ];
            $plugin = Plugin::create( $savedata );

            return response()->json([ 'message' => 'Plugin Added to your account', 'plugin' =>  $plugin ], 201 );
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
}
