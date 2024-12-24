<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class UserPluginsTableSeeder extends Seeder
{
    public function run()
    {
        $userPlugins = [
            [
                'user_id' => 1,
                'plugin_slug' => 'yoast-seo',
                'is_paid' => true,
                'paid_at' => now(),
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'user_id' => 1,
                'plugin_slug' => 'woocommerce',
                'is_paid' => true,
                'paid_at' => now(),
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'user_id' => 2,
                'plugin_slug' => 'wordfence',
                'is_paid' => true,
                'paid_at' => now(),
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('user_plugins')->insert($userPlugins);
    }
}
