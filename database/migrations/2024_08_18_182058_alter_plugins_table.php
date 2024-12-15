<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::table('plugins', function (Blueprint $table) {
            $table->string('version')->nullable();
            $table->boolean('is_active')->default(true);
        });
    }

    public function down()
    {
        Schema::table('plugins', function (Blueprint $table) {
            $table->dropColumn(['version', 'is_active']);
        });
    }
};
