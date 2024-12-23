<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreatePluginTagsTable extends Migration
{
    public function up()
    {
        Schema::create('plugin_tags', function (Blueprint $table) {
            $table->string('plugin_slug', 255);
            $table->string('tag_slug', 100);
            $table->timestamps();

            $table->primary(['plugin_slug', 'tag_slug']);

            // Foreign Key Constraints
            $table->foreign('plugin_slug')->references('slug')->on('plugins')->onDelete('cascade');
            $table->foreign('tag_slug')->references('slug')->on('tags')->onDelete('cascade');

            // Indexes
            $table->index('tag_slug');
        });
    }

    public function down()
    {
        Schema::dropIfExists('plugin_tags');
    }
}