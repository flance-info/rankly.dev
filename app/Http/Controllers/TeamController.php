<?php

namespace App\Http\Controllers;

use App\Models\Team;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Illuminate\Support\Facades\Auth;

class TeamController extends Controller {
    public function show( Team $team ) {
        $team->load( 'owner' ); // Ensure the owner relationship is loaded
        $availableRoles = [ 'Admin', 'Editor', 'Viewer' ]; // Example roles

        return Inertia::render( 'Teams/Show', [
            'team'           => $team,
            'availableRoles' => $availableRoles,
            'permissions'    => [
                'canDeleteTeam' => Auth::user()->can( 'delete', $team ),
                'canUpdateTeam' => Auth::user()->can( 'update', $team ),
            ],
        ] );
    }
}
