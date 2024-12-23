<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\File;

class UsersTableSeeder extends Seeder
{
    public function run()
    {
        $path = base_path('python/output/users.json'); // Adjust the path as necessary
        $data = json_decode(File::get($path), true);

        foreach ($data as $item) {
            if (isset($item['name']) && isset($item['email']) && isset($item['password'])) {
                User::updateOrCreate(
                    ['email' => $item['email']],
                    [
                        'name' => $item['name'],
                        'password' => Hash::make($item['password']) // Ensure passwords are hashed
                    ]
                );
            }
        }
    }
}