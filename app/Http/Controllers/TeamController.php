<?php

namespace App\Http\Controllers;

use App\Models\Team;
use Illuminate\Http\Request;
use Inertia\Inertia;

class TeamController extends Controller {
    /**
     * Display the specified team.
     *
     * @param \Illuminate\Http\Request $request
     * @param \App\Models\Team         $team
     *
     * @return \Inertia\Response
     */
    public function show( Request $request, Team $team ) {
        // Pass the team data to the Inertia component
        return Inertia::render( 'Teams/Show', [
            'team' => $team,
        ] );
    }
}
