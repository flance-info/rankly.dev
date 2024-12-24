<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PluginsTableSeeder extends Seeder
{
    public function run()
    {
        $plugins = [
            [
                'name' => 'Yoast SEO',
                'slug' => 'yoast-seo',
                'description' => 'The first true all-in-one SEO solution for WordPress',
                'plugin_data' => json_encode([
                    'version' => '20.0',
                    'requires' => '6.3',
                    'tested' => '6.4'
                ]),
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'WooCommerce',
                'slug' => 'woocommerce',
                'description' => 'An eCommerce toolkit that helps you sell anything',
                'plugin_data' => json_encode([
                    'version' => '8.3',
                    'requires' => '6.2',
                    'tested' => '6.4'
                ]),
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Wordfence Security',
                'slug' => 'wordfence',
                'description' => 'WordPress Security Plugin',
                'plugin_data' => json_encode([
                    'version' => '7.10',
                    'requires' => '6.0',
                    'tested' => '6.4'
                ]),
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('plugins')->insert($plugins);
    }
}
