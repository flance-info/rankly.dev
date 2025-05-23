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
            [
                'plugin_slug' => 'string-locator',
                'tag_slug' => 'find',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'string-locator',
                'tag_slug' => 'highlight',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'string-locator',
                'tag_slug' => 'search',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'string-locator',
                'tag_slug' => 'syntax',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'plugin_slug' => 'string-locator',
                'tag_slug' => 'text',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('plugin_tags')->insert($pluginTags);
    }
}
