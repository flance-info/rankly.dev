<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class PluginKeyword extends Model
{
    use HasFactory;

    protected $fillable = [
        'plugin_slug',
        'keyword',
        'occurrences',
        'language',
    ];

    public function plugin()
    {
        return $this->belongsTo(Plugin::class, 'plugin_slug', 'slug');
    }

    public function positions()
    {
        return $this->hasMany(KeywordPosition::class, 'keyword_id');
    }
} 