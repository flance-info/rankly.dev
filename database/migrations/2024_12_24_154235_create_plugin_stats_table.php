<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreatePluginStatsTable extends Migration
{
    public function up()
    {
        Schema::create('plugin_stats', function (Blueprint $table) {
            $table->id();
            $table->string('plugin_slug', 255);
            $table->date('stat_date');
            $table->integer('active_installs');
            $table->integer('support_threads')->default(0);
            $table->integer('support_threads_resolved')->default(0);
            $table->timestamps();

            // Unique constraint for plugin and date combination
            $table->unique(['plugin_slug', 'stat_date']);

            // Foreign key constraint
            $table->foreign('plugin_slug')
                  ->references('slug')
                  ->on('plugins')
                  ->onDelete('cascade');

            // Index for faster queries
            $table->index('stat_date');
            $table->index('plugin_slug');
        });
    }

    public function down()
    {
        Schema::dropIfExists('plugin_stats');
    }
} 