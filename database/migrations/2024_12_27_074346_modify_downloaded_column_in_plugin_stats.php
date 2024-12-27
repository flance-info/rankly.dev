<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        // First check if column exists
        if (!Schema::hasColumn('plugin_stats', 'downloaded')) {
            // Add column if it doesn't exist
            Schema::table('plugin_stats', function (Blueprint $table) {
                $table->bigInteger('downloaded')->default(0)->after('active_installs');
            });
        } else {
            // Modify existing column
            Schema::table('plugin_stats', function (Blueprint $table) {
                $table->bigInteger('downloaded')->default(0)->change();
            });
        }
    }
    
    public function down()
    {
        if (Schema::hasColumn('plugin_stats', 'downloaded')) {
            Schema::table('plugin_stats', function (Blueprint $table) {
                $table->integer('downloaded')->default(0)->change();
            });
        }
    }
};
