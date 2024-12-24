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
        ];

        DB::table('tags')->insert($tags);
    }
}
