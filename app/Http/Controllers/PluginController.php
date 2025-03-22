<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Models\Plugin;

// Assuming you have a Plugin model
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Session;
use Inertia\Inertia;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class PluginController extends Controller {
    public function searchPlugin( Request $request ) {
        $slug = $request->input( 'slug' );
        $slug = $this->getSlugFromUrl( $slug );
        
        if ( ! $slug ) {
            return response()->json( [ 'error' => 'No plugin slug or url provided' ], 400 );
        }
        
        if ( ! Auth::check() ) {
            return response()->json( [ 'error' => 'User not authenticated' ], 401 );
        }
        
        $userId = Auth::id();
        
        // Check if the plugin already exists for this user in user_plugins table
        $existingUserPlugin = DB::table('user_plugins')
            ->where('plugin_slug', $slug)
            ->where('user_id', $userId)
            ->first();
        
        if ( $existingUserPlugin ) {
            $plugin = Plugin::where('slug', $slug)->first();
            return response()->json([
                'message' => 'Plugin already added',
                'plugin' => $plugin
            ], 200);
        }

        // Query the WordPress.org API
        $response = Http::get( 'https://api.wordpress.org/plugins/info/1.2/', [
            'action'                       => 'plugin_information',
            'request[slug]'                => $slug,
            'request[fields][description]' => true
        ] );

        // Log the JSON response
        Log::info( 'WordPress API Response:', $response->json() );
        
        $pluginData = $response->json();
        
        if ( $pluginData && ! isset( $pluginData['error'] ) ) {
            return response()->json([
                'message' => 'Plugin Info received successfully',
                'plugin' => $pluginData
            ], 201);
        }

        return response()->json( [ 'error' => 'Plugin not found' ], 404 );
    }

    private function getSlugFromUrl( $input ) {
        if ( filter_var( $input, FILTER_VALIDATE_URL ) ) {
            $path     = parse_url( $input, PHP_URL_PATH );
            $path     = trim( $path, '/' );
            $segments = explode( '/', $path );

            return end( $segments );
        }

        return $input;
    }

    public function getSessionPlugins( Request $request ) {
        // Retrieve the current session data
        $currentPlugins = Session::get( 'plugin_data', [] );
        // Get the new plugins from the request
        $newPlugins = $request->input( 'plugins', [] );
        // Merge the current session data with the new plugins
        $updatedPlugins = array_merge( $currentPlugins, $newPlugins );
        // Update the session with the merged plugins list
        Session::put( 'plugin_data', $updatedPlugins );

        return response()->json( [ 'message' => 'Session plugins updated successfully', 'plugin_data' => $updatedPlugins ] );
    }

    public function store(Request $request)
    {
        if (!Auth::check()) {
            return response()->json(['error' => 'User not authenticated'], 401);
        }

        $pluginData = $plugin = $request->input('plugin');
        $userId = Auth::id();
        $slug = $plugin['slug'];

        // Check if the plugin exists in plugins table
        $existingPlugin = Plugin::where('slug', $slug)->first();

        // Check if user already has this plugin
        $existingUserPlugin = DB::table('user_plugins')
            ->where('plugin_slug', $slug)
            ->where('user_id', $userId)
            ->first();

        if ($pluginData && !isset($pluginData['error'])) {
            // Update or create the plugin record
            if ($existingPlugin) {
                $existingPlugin->update([
                    'name' => $pluginData['name'],
                    'plugin_data' => $pluginData,
                ]);
                $plugin = $existingPlugin;
            } else {
                $plugin = Plugin::create([
                    'name' => $pluginData['name'],
                    'slug' => $pluginData['slug'],
                    'plugin_data' => (array)$pluginData,
                ]);
            }

            // Create user-plugin relationship if it doesn't exist
            if (!$existingUserPlugin) {
                DB::table('user_plugins')->insert([
                    'user_id' => $userId,
                    'plugin_slug' => $slug,
                    'is_paid' => false,
                    'created_at' => now(),
                    'updated_at' => now(),
                ]);
                
                return response()->json([
                    'message' => 'Plugin Added to your account',
                    'plugin' => $pluginData
                ], 201);
            }

            return response()->json([
                'message' => 'Plugin updated successfully',
                'plugin' => $pluginData,
            ], 200);
        }

        return response()->json(['message' => 'Plugins added successfully to Your Account!']);
    }

    public function getUserPlugins(Request $request) {
        if (!Auth::check()) {
            return response()->json(['error' => 'User not authenticated'], 401);
        }

        $userId = Auth::id();
        
        // Get plugins through the user_plugins pivot table
        $plugins = Plugin::select('plugins.*', 'user_plugins.is_paid')
            ->join('user_plugins', 'plugins.slug', '=', 'user_plugins.plugin_slug')
            ->where('user_plugins.user_id', $userId)
            ->with(['tags', 'latestStats']) // Optional: Include related data
            ->get();

        return response()->json($plugins);
    }

    public function destroy($slug)
    {
        if (!Auth::check()) {
            return response()->json(['error' => 'User not authenticated'], 401);
        }

        $userId = Auth::id();
        
        // Delete from user_plugins table instead of plugins table
        $deleted = DB::table('user_plugins')
            ->where('plugin_slug', $slug)
            ->where('user_id', $userId)
            ->delete();

        if (!$deleted) {
            return response()->json(['error' => 'Plugin not found'], 404);
        }

        return response()->json(['message' => 'Plugin deleted successfully'], 200);
    }

    public function show($slug) {
        // Check if the user is authenticated
        if (!Auth::check()) {
            return redirect()->route('login');
        }

        // Fetch the plugin by slug
        $plugin = Plugin::where('slug', $slug)->first();



        if ($plugin) {
            // Return an Inertia response with the plugin data
            return Inertia::render('PluginPage', [
                'plugin' => $plugin
            ]);
        } else {
            // Optionally, redirect or show an error page
            return redirect()->route('plugins.index')->with('error', 'Plugin not found');
        }
    }

    public function getActiveInstalls($slug, Request $request)
    {
        try {
            $plugin = Plugin::where('slug', $slug)->first();
            
            if (!$plugin) {
                return response()->json([
                    'success' => false,
                    'message' => 'Plugin not found'
                ], 404);
            }

            // Get trend value from request, default to 7 days
            $trend = $request->input('trend', '7');
            
            // Convert trend to integer for date calculation
            $days = match($trend) {
                '7' => 7,
                '15' => 15,
                '30' => 30,
                '90' => 90,
                default => 7,
            };

            // Get stats based on trend
            $stats = DB::table('plugin_stats')
                ->where('plugin_slug', $slug)
                ->where('stat_date', '>=', Carbon::now()->subDays($days))
                ->orderBy('stat_date', 'asc')
                ->get(['stat_date', 'active_installs']);

            $data = [];
            foreach ($stats as $stat) {
                $data[Carbon::parse($stat->stat_date)->format('M d')] = $stat->active_installs;
            }

            // Calculate percentage change
            $firstValue = array_values($data)[0] ?? 0;
            $lastValue = end($data) ?? 0;
            $percentageChange = $firstValue > 0 ? 
                round((($lastValue - $firstValue) / $firstValue) * 100, 2) : 0;

            // Get total active installs from plugin data
            $totalActiveInstalls = $plugin->plugin_data['active_installs'] ?? 0;

            return response()->json([
                'success' => true,
                'data' => $data,
                'summary' => [
                    'total_active_installs' => $totalActiveInstalls,
                    'percentage_change' => $percentageChange
                ]
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error fetching active installs data'
            ], 500);
        }
    }

    private function calculatePercentageChange($data)
    {
        if (count($data) < 2) {
            return 0;
        }

        $values = array_values($data);
        $first = $values[0];
        $last = end($values);

        if ($first == 0) {
            return 0;
        }

        return round((($last - $first) / $first) * 100, 2);
    }

    public function getPositionMovement(Request $request)
    {
        try {
            // Display current database connection info
            $connection = DB::connection();
            $currentDatabase = $connection->getDatabaseName();
            $currentHost = $connection->getConfig('host');
            /*
           dd("Database Connection Info:", [
                'database' => $currentDatabase,
                'host' => $currentHost,
                'driver' => $connection->getConfig('driver')
            ]);
            */
            $slug = $request->input('slug');
            $keywords = $request->input('keywords');
            $trend = $request->input('trend', '7');

            $days = match($trend) {
                '7' => 7,
                '15' => 15,
                '30' => 30,
                '90' => 90,
                '365' => 365,
                default => 7,
            };

            // Step 1: Get plugin_id from slug
            $pluginId = DB::table('plugins')
                ->where('slug', $slug)
                ->value('id');
            
            if (!$pluginId) {
                return response()->json(['error' => 'Plugin not found'], 404);
            }
            
            // Step 2: Get keyword_ids from slugs
            $keywordIds = DB::table('keywords')
                ->whereIn('slug', $keywords)
                ->pluck('id')
                ->toArray();
            
            if (empty($keywordIds)) {
                return response()->json(['error' => 'No matching keywords found'], 404);
            }
            
            // Step 3: Execute the main query with IDs instead of slugs
            $rawData = DB::table('plugin_keyword_stats')
                ->select('keyword_id', 'rank_order', 'stat_date')
                ->where('plugin_id', $pluginId)
                ->whereIn('keyword_id', $keywordIds)
                ->where('stat_date', '>=', DB::raw("now() - interval '{$days} days'"))  // TimescaleDB optimized
                ->orderBy('stat_date', 'asc')
                ->get();

            // Calculate averages for each date
            $averagesByDate = [];
            foreach ($rawData as $record) {
                $date = $record->stat_date;
                if (!isset($averagesByDate[$date])) {
                    $averagesByDate[$date] = [
                        'total' => 0,
                        'count' => 0,
                    ];
                }
                $averagesByDate[$date]['total'] += $record->rank_order;
                $averagesByDate[$date]['count']++;
            }

            // Format the response data
            $averagedData = [];
            foreach ($averagesByDate as $date => $values) {
                $averagedData[] = [
                    'stat_date' => $date,
                    'rank_order' => round($values['total'] / $values['count'], 2),
                    'raw_data' => $rawData->where('stat_date', $date)->values()
                ];
            }

            return response()->json([
                'success' => true,
                'data' => $averagedData
            ]);
        } catch (\Exception $e) {
            return response()->json(['success' => false, 'message' => 'Failed to fetch data'], 500);
        }
    }

    public function getPluginData($slug)
    {
        try {
            // Fetch plugin data from the database
            $plugin = Plugin::where('slug', $slug)->first();

            if ($plugin) {
                return response()->json(['success' => true, 'data' => $plugin]);
            } else {
                return response()->json(['success' => false, 'message' => 'Plugin not found'], 404);
            }
        } catch (\Exception $e) {
            return response()->json(['success' => false, 'message' => 'Failed to fetch plugin data'], 500);
        }
    }
}

