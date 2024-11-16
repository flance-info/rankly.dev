<?php

use App\Http\Controllers\PluginController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::middleware(
    'auth:sanctum')->post('/search-plugin',
    [PluginController::class, 'searchPlugin'])->name('search-plugin');

Route::post('/update-session-plugins', [PluginController::class, 'updateSessionPlugins']);

Route::get('/session-plugins', [PluginController::class, 'getSessionPlugins']);


Route::post('/api/user/plugins', [PluginController::class, 'store']);
Route::middleware(
    'auth:sanctum')->post('/user/plugin',  [PluginController::class, 'store']);




