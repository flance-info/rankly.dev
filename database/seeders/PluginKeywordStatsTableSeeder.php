<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PluginKeywordStatsTableSeeder extends Seeder
{
    public function run()
    {
        $stats = [
            [
                'plugin_slug' => 'yoast-seo',
                'keyword_slug' => 'seo',
                'stat_date' => '2024-03-20',
                'rank_order' => 1,
                'active_installs' => 5000000,
                'rating' => 4.8,
                'num_ratings' => 28500,
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'woocommerce',
                'keyword_slug' => 'ecommerce',
                'stat_date' => '2024-03-20',
                'rank_order' => 1,
                'active_installs' => 8000000,
                'rating' => 4.5,
                'num_ratings' => 35000,
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'wordfence',
                'keyword_slug' => 'security',
                'stat_date' => '2024-03-20',
                'rank_order' => 1,
                'active_installs' => 4000000,
                'rating' => 4.7,
                'num_ratings' => 25000,
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('plugin_keyword_stats')->insert($stats);
    }
}
