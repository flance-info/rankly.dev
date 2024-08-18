<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class EnsureCurrentTeamIsSet
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle(Request $request, Closure $next)
    {
        $user = Auth::user();

        // Check if current_team is not set and if the user has any teams
        if (!$user->current_team && $user->all_teams->isNotEmpty()) {
            // Set the first team as the current team
            $user->current_team = $user->all_teams->first();
            $user->save(); // Persist the change to the database
        }

        return $next($request);
    }
}

