<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PluginStatsTableSeeder extends Seeder
{
    public function run()
    {
        $stats = [
            [
                'plugin_slug' => 'yoast-seo',
                'stat_date' => '2024-03-20',
                'active_installs' => 5000000,
                'support_threads' => 125,
                'support_threads_resolved' => 98,
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'yoast-seo',
                'stat_date' => '2024-03-19',
                'active_installs' => 4950000,
                'support_threads' => 120,
                'support_threads_resolved' => 95,
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'woocommerce',
                'stat_date' => '2024-03-20',
                'active_installs' => 8000000,
                'support_threads' => 250,
                'support_threads_resolved' => 180,
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'wordfence',
                'stat_date' => '2024-03-20',
                'active_installs' => 4000000,
                'support_threads' => 75,
                'support_threads_resolved' => 65,
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('plugin_stats')->insert($stats);
    }
} 