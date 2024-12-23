<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        // First, ensure there are no duplicate slugs
        DB::statement('
            DELETE FROM plugins a USING plugins b 
            WHERE a.id > b.id 
            AND a.slug = b.slug
        ');

        // Changed from 'plugin_slug' to 'slug'
        Schema::table('plugins', function (Blueprint $table) {
            $table->unique('slug');  // This is the correct column name
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('plugins', function (Blueprint $table) {
            $table->dropUnique(['slug']);  // This should match the column name too
        });
    }
};
