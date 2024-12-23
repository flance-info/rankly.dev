<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('plugins', function (Blueprint $table) {
            $table->bigIncrements('id');                         // Primary Key
            $table->string('name', 255);                         // Plugin Name
            $table->string('slug', 255)->unique();               // Unique Slug
            $table->text('description')->nullable();             // Plugin Description
            $table->json('plugin_data')->nullable();             // Additional Data
            $table->timestamps();                                // created_at & updated_at
        });
    }

    public function down()
    {
        Schema::dropIfExists('plugins');
    }
};
