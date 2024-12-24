<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PluginStat extends Model
{
    protected $table = 'plugin_stats';

    protected $fillable = [
        'plugin_slug',
        'stat_date',
        'active_installs',
        'support_threads',
        'support_threads_resolved'
    ];

    protected $casts = [
        'stat_date' => 'date',
        'active_installs' => 'integer',
        'support_threads' => 'integer',
        'support_threads_resolved' => 'integer'
    ];

    // Relationship with Plugin
    public function plugin()
    {
        return $this->belongsTo(Plugin::class, 'plugin_slug', 'slug');
    }
} 