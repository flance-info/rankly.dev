<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class PluginStatsTableSeeder extends Seeder
{
    public function run()
    {
        $stats = [];
        $plugins = ['yoast-seo', 'woocommerce', 'wordfence', 'string-locator'];
        
        // Base stats for each plugin
        $baseStats = [
            'yoast-seo' => [
                'active_installs' => 5000000,
                'support_threads' => 125,
                'support_threads_resolved' => 98,
            ],
            'woocommerce' => [
                'active_installs' => 8000000,
                'support_threads' => 250,
                'support_threads_resolved' => 180,
            ],
            'wordfence' => [
                'active_installs' => 4000000,
                'support_threads' => 75,
                'support_threads_resolved' => 65,
            ],
            'string-locator' => [
                'active_installs' => 100000,
                'support_threads' => 0,
                'support_threads_resolved' => 0,
            ],
        ];

        // Generate last 30 days of data
        for ($i = 30; $i >= 0; $i--) {
            $date = Carbon::now()->subDays($i)->format('Y-m-d');
            
            foreach ($plugins as $plugin) {
                $baseActiveInstalls = $baseStats[$plugin]['active_installs'];
                
                // Add some random variation to active_installs (±2%)
                $variation = rand(-20, 20) / 1000; // Convert to percentage
                $activeInstalls = round($baseActiveInstalls * (1 + $variation));
                
                // Add some random variation to support threads
                $baseThreads = $baseStats[$plugin]['support_threads'];
                $supportThreads = rand(
                    max(0, $baseThreads - 5),
                    $baseThreads + 5
                );
                
                // Resolved threads should be less than or equal to total threads
                $baseResolved = $baseStats[$plugin]['support_threads_resolved'];
                $supportThreadsResolved = min(
                    $supportThreads,
                    rand(
                        max(0, $baseResolved - 5),
                        $baseResolved + 5
                    )
                );

                $stats[] = [
                    'plugin_slug' => $plugin,
                    'stat_date' => $date,
                    'active_installs' => $activeInstalls,
                    'support_threads' => $supportThreads,
                    'support_threads_resolved' => $supportThreadsResolved,
                    'created_at' => now(),
                    'updated_at' => now(),
                ];
            }
        }

        // Insert all stats
        DB::table('plugin_stats')->insert($stats);
    }
} 