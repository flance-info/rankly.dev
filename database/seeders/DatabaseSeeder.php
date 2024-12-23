<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run()
    {
        $this->call([
            UsersTableSeeder::class,
            KeywordsTableSeeder::class,
            PluginsTableSeeder::class,
            TagsTableSeeder::class,
            PluginKeywordStatsTableSeeder::class,
            PluginTagsTableSeeder::class,
            UserPluginsTableSeeder::class, // New seeder for user-plugin associations
        ]);
    }
}