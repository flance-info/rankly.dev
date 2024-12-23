<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Plugin;
use Illuminate\Support\Facades\File;
use Carbon\Carbon;

class UserPluginsTableSeeder extends Seeder
{
    public function run()
    {
        $path = base_path('python/output/user_plugins.json'); // Adjust the path as necessary
        $data = json_decode(File::get($path), true);

        foreach ($data as $item) {
            if (isset($item['user_email']) && isset($item['plugin_slug'])) {
                $user = User::where('email', $item['user_email'])->first();
                $plugin = Plugin::where('slug', $item['plugin_slug'])->first();

                if ($user && $plugin) {
                    $user->plugins()->updateOrCreate(
                        ['plugin_slug' => $plugin->slug],
                        [
                            'is_paid' => $item['is_paid'] ?? false,
                            'paid_at' => isset($item['paid_at']) ? Carbon::parse($item['paid_at']) : null
                        ]
                    );
                }
            }
        }
    }
}
