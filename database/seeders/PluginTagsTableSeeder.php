<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PluginTagsTableSeeder extends Seeder
{
    public function run()
    {
        $pluginTags = [
            [
                'plugin_slug' => 'yoast-seo',
                'tag_slug' => 'seo',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'yoast-seo',
                'tag_slug' => 'performance',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'woocommerce',
                'tag_slug' => 'ecommerce',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'wordfence',
                'tag_slug' => 'security',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('plugin_tags')->insert($pluginTags);
    }
}
