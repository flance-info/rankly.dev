<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PluginsTableSeeder extends Seeder
{
    public function run()
    {
        $plugins = [
            [
                'name' => 'Yoast SEO',
                'slug' => 'yoast-seo',
                'description' => 'The first true all-in-one SEO solution for WordPress',
                'plugin_data' => json_encode([
                    'version' => '20.0',
                    'requires' => '6.3',
                    'tested' => '6.4'
                ]),
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'WooCommerce',
                'slug' => 'woocommerce',
                'description' => 'An eCommerce toolkit that helps you sell anything',
                'plugin_data' => json_encode([
                    'version' => '8.3',
                    'requires' => '6.2',
                    'tested' => '6.4'
                ]),
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Wordfence Security',
                'slug' => 'wordfence',
                'description' => 'WordPress Security Plugin',
                'plugin_data' => json_encode([
                    'version' => '7.10',
                    'requires' => '6.0',
                    'tested' => '6.4'
                ]),
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'String locator',
                'slug' => 'string-locator',
                'description' => 'Search through files in WordPress, directly from your WordPress admin.',
                'plugin_data' => json_encode([
                    'version' => '2.6.6',
                    'author' => '<a href="https://instawp.com/">InstaWP</a>',
                    'author_profile' => 'https://profiles.wordpress.org/instawp/',
                    'requires' => '4.9',
                    'tested' => '6.6.2',
                    'requires_php' => false,
                    'contributors' => [
                        'instawp' => [
                            'profile' => 'https://profiles.wordpress.org/instawp/',
                            'avatar' => 'https://secure.gravatar.com/avatar/b41b495c02caa2203cb0176cc4638d6a?s=96&d=monsterid&r=g',
                            'display_name' => 'InstaWP'
                        ],
                        'clorith' => [
                            'profile' => 'https://profiles.wordpress.org/clorith/',
                            'avatar' => 'https://secure.gravatar.com/avatar/8f2a6a1a5388876ac51cd6dde3b4a1d0?s=96&d=monsterid&r=g',
                            'display_name' => 'Marius L. J.'
                        ]
                    ],
                    'requires' => '4.9',
                   'tested' => '6.6.2',
                   'requires_php' => false,
                   'requires_plugins' => [],
                   'rating' => 92,
                   'ratings' => [
                       '5' => 108,
                       '4' => 0,
                       '3' => 1,
                       '2' => 2,
                       '1' => 10
                   ],
                   'num_ratings' => 121,
                   'support_threads' => 0,
                   'support_threads_resolved' => 0,
                   'active_installs' => 100000,
                    'last_updated' => '2024-08-21 3:03pm GMT',
                    'added' => '2013-08-15',
                    'download_link' => 'https://downloads.wordpress.org/plugin/string-locator.2.6.6.zip',
                    'homepage' => 'https://wordpress.org/plugins/string-locator/'
                ]),
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('plugins')->insert($plugins);
    }
}
