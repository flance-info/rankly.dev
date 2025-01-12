<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddDownloadedColumnToPluginKeywordStatsTable extends Migration
{
    public function up()
    {
        Schema::table('plugin_keyword_stats', function (Blueprint $table) {
            $table->integer('downloaded')->default(0); // Add the new column with a default value
        });
    }

    public function down()
    {
        Schema::table('plugin_keyword_stats', function (Blueprint $table) {
            $table->dropColumn('downloaded'); // Remove the column if rolling back
        });
    }
} 