<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        // First check if the column exists
        if (Schema::hasColumn('keywords', 'keyword_slug')) {
            // Remove any duplicate slugs using the correct column name
            DB::statement('
                DELETE FROM keywords a USING keywords b 
                WHERE a.id > b.id 
                AND a.slug = b.slug
            ');

            Schema::table('keywords', function (Blueprint $table) {
                $table->unique('slug');
            });
        } else {
            // If the column doesn't exist, add it
            Schema::table('keywords', function (Blueprint $table) {
                $table->string('slug', 100)->unique();
            });
        }
    }

    public function down(): void
    {
        Schema::table('keywords', function (Blueprint $table) {
            if (Schema::hasColumn('keywords', 'slug')) {
                $table->dropUnique(['slug']);
            }
        });
    }
};