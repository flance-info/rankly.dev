<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreatePluginKeywordStatsTable extends Migration
{
    public function up()
    {
        Schema::create('plugin_keyword_stats', function (Blueprint $table) {
            $table->id();
            $table->string('plugin_slug', 255);
            $table->string('keyword_slug', 100);
            $table->date('stat_date');
            $table->integer('rank_order');
            $table->integer('active_installs')->nullable();
            $table->decimal('rating', 3, 2)->nullable();
            $table->integer('num_ratings')->nullable();
            $table->timestamps();

            $table->unique(['plugin_slug', 'keyword_slug', 'stat_date']);

            // Foreign Key Constraints
            $table->foreign('plugin_slug')->references('slug')->on('plugins')->onDelete('cascade');
            $table->foreign('keyword_slug')->references('slug')->on('keywords')->onDelete('cascade');

            // Indexes
            $table->index('stat_date');
            $table->index('keyword_slug');
            $table->index('plugin_slug');
        });
    }

    public function down()
    {
        Schema::dropIfExists('plugin_keyword_stats');
    }
}