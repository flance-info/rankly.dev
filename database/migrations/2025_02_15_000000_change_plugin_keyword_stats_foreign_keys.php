<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

class ChangePluginKeywordStatsForeignKeys extends Migration
{
    public function up()
    {
        DB::transaction(function () {
            Schema::table('plugin_keyword_stats', function (Blueprint $table) {
                // Add new columns
                $table->unsignedBigInteger('plugin_id');
                $table->unsignedBigInteger('keyword_id');
                
                // Add temporary indexes if columns exist
                if (Schema::hasColumn('plugin_keyword_stats', 'plugin_slug')) {
                    $table->index('plugin_slug');
                }
                if (Schema::hasColumn('plugin_keyword_stats', 'keyword_slug')) {
                    $table->index('keyword_slug');
                }
            });

            // Populate new columns with IDs
            DB::statement('
                UPDATE plugin_keyword_stats pks
                SET 
                    plugin_id = p.id,
                    keyword_id = k.id
                FROM plugins p
                JOIN keywords k 
                    ON pks.plugin_slug = p.slug
                    AND pks.keyword_slug = k.slug
            ');

            Schema::table('plugin_keyword_stats', function (Blueprint $table) {
                // Remove old foreign keys
                $table->dropForeign(['plugin_slug']);
                $table->dropForeign(['keyword_slug']);
                
                // Add new foreign keys
                $table->foreign('plugin_id')
                    ->references('id')
                    ->on('plugins')
                    ->onDelete('cascade');

                $table->foreign('keyword_id')
                    ->references('id')
                    ->on('keywords')
                    ->onDelete('cascade');

                // Drop old slug columns
                $table->dropColumn(['plugin_slug', 'keyword_slug']);
            });
        });
    }

    public function down()
    {
        // Reverse operations if needed
    }
} 