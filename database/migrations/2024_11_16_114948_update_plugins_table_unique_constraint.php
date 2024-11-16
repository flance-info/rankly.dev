<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class UpdatePluginsTableUniqueConstraint extends Migration
{
    public function up()
    {
        Schema::table('plugins', function (Blueprint $table) {
            $table->dropUnique(['slug']); // Drop the existing unique constraint
            $table->unique(['slug', 'user_id']); // Add a composite unique constraint
        });
    }

    public function down()
    {
        Schema::table('plugins', function (Blueprint $table) {
            $table->dropUnique(['slug', 'user_id']); // Remove the composite unique constraint
            $table->unique('slug'); // Re-add the original unique constraint
        });
    }
}

