<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class UserKeyword extends Model
{
    protected $fillable = [
        'user_id',
        'plugin_slug',
        'keyword_slug',
        'status'
    ];

    protected $attributes = [
        'status' => 'published'
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
} 