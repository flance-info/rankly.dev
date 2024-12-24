<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class KeywordsTableSeeder extends Seeder
{
    public function run()
    {
        $keywords = [
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
                'slug' => 'optimization',
                'name' => 'Optimization',
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
                'slug' => 'backup',
                'name' => 'Backup',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('keywords')->insert($keywords);
    }
}
