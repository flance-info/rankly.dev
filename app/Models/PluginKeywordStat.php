<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PluginKeywordStat extends Model
{
    use HasFactory;

    protected $fillable = [
        'plugin_slug',
        'keyword',
        'rank_order',
        'language',
        'created_at'
    ];

    /**
     * Get the plugin associated with the statistic.
     */
    public function plugin()
    {
        return $this->belongsTo(Plugin::class, 'plugin_slug', 'slug');
    }
}