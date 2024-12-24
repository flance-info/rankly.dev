<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Plugin extends Model
{
    protected $primaryKey = 'slug';
    public $incrementing = false;
    protected $keyType = 'string';

    protected $fillable = [
        'slug',
        'name',
        'description',
        'plugin_data'
    ];

    // Relationship with users through user_plugins table
    public function users()
    {
        return $this->belongsToMany(User::class, 'user_plugins', 'plugin_slug', 'user_id')
                    ->withPivot('is_paid', 'paid_at')
                    ->withTimestamps();
    }

    // Get tags for the plugin
    public function tags()
    {
        return $this->belongsToMany(Tag::class, 'plugin_tags', 'plugin_slug', 'tag_slug', 'slug', 'slug');
    }

    // Get latest stats for the plugin
    public function latestStats()
    {
        return $this->hasOne(PluginStat::class, 'plugin_slug', 'slug')
                    ->latest('stat_date');
    }

    // Get all stats for the plugin
    public function stats()
    {
        return $this->hasMany(PluginStat::class, 'plugin_slug', 'slug');
    }
}

