<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class UpdatePluginsTableAddPluginDataColumn extends Migration
{
    public function up()
    {
        Schema::table('plugins', function (Blueprint $table) {
            $table->json('plugin_data')->nullable(); // Add a JSON column to store all plugin data
        });
    }

    public function down()
    {
        Schema::table('plugins', function (Blueprint $table) {
            $table->dropColumn('plugin_data'); // Rollback the column
        });
    }
}


