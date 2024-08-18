<?php

use App\Http\Controllers\PluginController;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;
use App\Http\Controllers\Admin\AdminController;
use App\Http\Controllers\User\UserController;
use App\Http\Controllers\TeamController;
/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return Inertia::render('Welcome', [
        'canLogin' => Route::has('login'),
        'canRegister' => Route::has('register'),
        'laravelVersion' => Application::VERSION,
        'phpVersion' => PHP_VERSION,
    ]);
});

// User Routes
Route::middleware([
    'auth:sanctum',
    config('jetstream.auth_session'),
    'verified',
])->group(function () {
    Route::get('/dashboard', [UserController::class, 'index'])->name('dashboard');
   Route::get('/dashboard/add-plugin', function () {
            return Inertia::render('AddPlugin');
        })->name('add-plugin');
});

// Admin Routes
Route::middleware(['auth', 'admin'])->group(function () {
    Route::get('/admin/dashboard', [AdminController::class, 'index'])->name('admin.dashboard');
    // Other admin routes
});



Route::middleware(['auth', 'ensure.current_team'])->group(function () {
    Route::get('/teams/{team}', [TeamController::class, 'show'])->name('teams.show');
    // Other routes that require current_team
});

Route::post('/search-plugin', [PluginController::class, 'searchPlugin'])->name('search-plugin');



