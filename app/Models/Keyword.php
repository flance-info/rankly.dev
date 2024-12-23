<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Keyword extends Model
{
    use HasFactory;

    protected $fillable = ['slug', 'name'];

    /**
     * Get the plugin keyword stats for the keyword.
     */
    public function pluginKeywordStats()
    {
        return $this->hasMany(PluginKeywordStat::class, 'keyword_slug', 'slug');
    }
}
