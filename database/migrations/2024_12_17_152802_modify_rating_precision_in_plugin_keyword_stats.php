<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class ModifyRatingPrecisionInPluginKeywordStats extends Migration
{
    public function up()
    {
        Schema::table('plugin_keyword_stats', function (Blueprint $table) {
            $table->decimal('rating', 10, 2)->change(); // Adjust precision and scale to 10, 2
        });
    }

    public function down()
    {
        Schema::table('plugin_keyword_stats', function (Blueprint $table) {
            $table->decimal('rating', 3, 2)->change(); // Revert to original precision and scale
        });
    }
} 