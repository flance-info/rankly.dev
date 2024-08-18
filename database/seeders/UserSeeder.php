<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Spatie\Permission\Models\Role;

class UserSeeder extends Seeder
{
    public function run()
    {
        // Create an admin user and assign the 'admin' role
        $user = User::create([
            'name' => 'Admin User 1',
            'email' => 'admin1@example.com',
            'password' => bcrypt('password'),
        ]);

        $user->assignRole('admin');

         $user = User::create([
            'name' => 'User',
            'email' => 'user@example.com',
            'password' => bcrypt('password'),
        ]);

        $user->assignRole('user');
    }
}
