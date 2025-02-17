<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class RemoveTimestamps extends Migration
{
    public function up()
    {
        Schema::table('plugin_keyword_stats', function (Blueprint $table) {
            $table->dropColumn(['created_at', 'updated_at']);
        });
    }

    public function down()
    {
        Schema::table('plugin_keyword_stats', function (Blueprint $table) {
            $table->timestamps();
        });
    }
} 