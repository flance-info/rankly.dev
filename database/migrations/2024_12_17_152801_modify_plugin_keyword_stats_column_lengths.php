<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class ModifyPluginKeywordStatsColumnLengths extends Migration
{
    public function up()
    {
        Schema::table('plugin_keyword_stats', function (Blueprint $table) {
            $table->string('plugin_slug', 1000)->change(); // Change column length to 1000
            $table->string('keyword_slug', 1000)->change(); // Change column length to 1000
        });
    }

    public function down()
    {
        Schema::table('plugin_keyword_stats', function (Blueprint $table) {
            $table->string('plugin_slug', 255)->change(); // Revert column length to 255
            $table->string('keyword_slug', 100)->change(); // Revert column length to 100
        });
    }
} 