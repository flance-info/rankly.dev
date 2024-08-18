<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class UpdateTeamsTable extends Migration
{
    public function up()
    {
        Schema::table('teams', function (Blueprint $table) {
            $table->boolean('personal_team')->default(false)->change();
        });
    }

    public function down()
    {
        Schema::table('teams', function (Blueprint $table) {
            $table->boolean('personal_team')->change();
        });
    }
}

