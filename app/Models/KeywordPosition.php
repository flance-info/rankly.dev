<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class KeywordPosition extends Model
{
    use HasFactory;

    protected $fillable = [
        'keyword_id',
        'position',
        'created_at'
    ];

    public function keyword()
    {
        return $this->belongsTo(PluginKeyword::class);
    }
} 