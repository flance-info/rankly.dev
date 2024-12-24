<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class TagsTableSeeder extends Seeder
{
    public function run()
    {
        $tags = [
            [
                'slug' => 'performance',
                'name' => 'Performance',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'slug' => 'security',
                'name' => 'Security',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'slug' => 'seo',
                'name' => 'SEO',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'slug' => 'ecommerce',
                'name' => 'eCommerce',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'slug' => 'find',
                'name' => 'Find',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'slug' => 'highlight',
                'name' => 'Highlight',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'slug' => 'search',
                'name' => 'Search',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'slug' => 'syntax',
                'name' => 'Syntax',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'slug' => 'text',
                'name' => 'Text',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('tags')->insert($tags);
    }
}
