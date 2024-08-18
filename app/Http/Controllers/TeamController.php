<?php

namespace App\Http\Controllers;

use App\Models\Team;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Illuminate\Support\Facades\Auth;

class TeamController extends Controller
{
    public function show(Team $team)
    {
        $availableRoles = ['Admin', 'Editor', 'Viewer']; // Example roles

        return Inertia::render('Teams/Show', [
            'team' => $team,
            'availableRoles' => $availableRoles,
            'permissions' => [
                'canDeleteTeam' => Auth::user()->can('delete', $team),
                // Add other permission checks here as needed
            ],
        ]);
    }
}
