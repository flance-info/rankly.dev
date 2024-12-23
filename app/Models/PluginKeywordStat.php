<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PluginKeywordStat extends Model
{
    use HasFactory;

    protected $fillable = [
        'plugin_slug',
        'keyword_slug',
        'stat_date',
        'rank_order',
        'active_installs',
        'rating',
        'num_ratings'
    ];

    /**
     * Get the plugin associated with the statistic.
     */
    public function plugin()
    {
        return $this->belongsTo(Plugin::class, 'plugin_slug', 'slug');
    }

    /**
     * Get the keyword associated with the statistic.
     */
    public function keyword()
    {
        return $this->belongsTo(Keyword::class, 'keyword_slug', 'slug');
    }
}