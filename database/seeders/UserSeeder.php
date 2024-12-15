<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    public function run()
    {
        // Define the users you want to create
        $users = [
            [
                'name' => 'Admin User 1',
                'email' => 'admin1@example.com',
                'password' => 'password',
            ],
            [
                'name' => 'tutyou1972',
                'email' => 'tutyou1972@gmail.com',
                'password' => 'password',
            ]
        ];

        // Create users if they don't exist
        foreach ($users as $userData) {
            User::updateOrCreate(
                ['email' => $userData['email']], // Check if email exists
                [
                    'name' => $userData['name'],
                    'password' => Hash::make($userData['password']),
                ]
            );
        }

        $this->command->info('Users seeded successfully!');
    }
}
