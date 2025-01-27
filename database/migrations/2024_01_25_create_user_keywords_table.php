<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('user_keywords', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('plugin_slug');
            $table->string('keyword_slug');
            $table->timestamps();
            
            // Unique constraint to prevent duplicates
            $table->unique(['user_id', 'plugin_slug', 'keyword_slug']);
        });
    }

    public function down()
    {
        Schema::dropIfExists('user_keywords');
    }
}; 