<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Plugin extends Model {
    use HasFactory;

    protected $fillable
        = [
            'name',
            'slug',
            'user_id',
            'plugin_data',
        ];

    protected $casts
        = [
            'plugin_data' => 'array',
        ];

        /**
     * The users that own the plugin.
     */
    public function users()
    {
        return $this->belongsToMany(User::class, 'user_plugins', 'plugin_slug', 'user_id')
                    ->using(UserPlugin::class)
                    ->withPivot('is_paid', 'paid_at')
                    ->withTimestamps();
    }

    /**
     * Get the keyword stats for the plugin.
     */
    public function pluginKeywordStats()
    {
        return $this->hasMany(PluginKeywordStat::class, 'plugin_slug', 'slug');
    }

    /**
     * The tags that belong to the plugin.
     */
    public function tags()
    {
        return $this->belongsToMany(Tag::class, 'plugin_tags', 'plugin_slug', 'tag_slug');
    }
}

