<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\File;

class KeywordsTableSeeder extends Seeder
{
    public function run()
    {
        $json = File::get(database_path('seeders/json/keywords.json'));
        $data = json_decode($json);

        foreach ($data as $item) {
            DB::table('keywords')->insert([
                'slug' => $item->slug,
                'name' => $item->name,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }
}
