<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class UserPlugin extends Pivot
{
    protected $table = 'user_plugins';

    protected $fillable = [
        'user_id',
        'plugin_slug',
        'is_paid',
        'paid_at'
    ];

    protected $dates = [
        'paid_at',
        'created_at',
        'updated_at',
    ];
}
