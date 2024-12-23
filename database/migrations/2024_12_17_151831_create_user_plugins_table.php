<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateUserPluginsTable extends Migration
{
    public function up()
    {
        Schema::create('user_plugins', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('user_id');                // FK to users.id
            $table->string('plugin_slug', 255);                   // FK to plugins.slug
            $table->boolean('is_paid')->default(false);           // Payment status
            $table->timestamp('paid_at')->nullable();             // Payment timestamp
            $table->timestamps();

            $table->unique(['user_id', 'plugin_slug']);

            // Foreign Key Constraints
            $table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
            $table->foreign('plugin_slug')->references('slug')->on('plugins')->onDelete('cascade');

            // Indexes
            $table->index('user_id');
            $table->index('plugin_slug');
        });
    }

    public function down()
    {
        Schema::dropIfExists('user_plugins');
    }
}