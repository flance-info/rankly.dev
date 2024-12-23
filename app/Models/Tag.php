<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    use HasFactory;

    protected $fillable = ['slug', 'label'];

    /**
     * The plugins that belong to the tag.
     */
    public function plugins()
    {
        return $this->belongsToMany(Plugin::class, 'plugin_tags', 'tag_slug', 'plugin_slug');
    }
}