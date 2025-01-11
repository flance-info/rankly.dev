<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

class UpdateTagsVarcharLengthV2 extends Migration
{
    public function up()
    {
        try {
            DB::statement('ALTER TABLE tags ALTER COLUMN slug TYPE varchar(1000)');
            DB::statement('ALTER TABLE tags ALTER COLUMN name TYPE varchar(1000)');
            
            DB::statement('ALTER TABLE keywords ALTER COLUMN slug TYPE varchar(1000)');
            DB::statement('ALTER TABLE keywords ALTER COLUMN name TYPE varchar(1000)');
            
            DB::statement('ALTER TABLE plugin_tags ALTER COLUMN tag_slug TYPE varchar(1000)');
            
            echo "Successfully updated column lengths to 1000\n";
        } catch (\Exception $e) {
            echo "Error: " . $e->getMessage() . "\n";
            throw $e;
        }
    }

    public function down()
    {
        DB::statement('ALTER TABLE tags ALTER COLUMN slug TYPE varchar(100)');
        DB::statement('ALTER TABLE tags ALTER COLUMN name TYPE varchar(100)');
        
        DB::statement('ALTER TABLE keywords ALTER COLUMN slug TYPE varchar(100)');
        DB::statement('ALTER TABLE keywords ALTER COLUMN name TYPE varchar(100)');
        
        DB::statement('ALTER TABLE plugin_tags ALTER COLUMN tag_slug TYPE varchar(100)');
    }
} 