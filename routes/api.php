<?php

use App\Http\Controllers\PluginController;
use App\Http\Controllers\PluginStatsController;
use App\Http\Controllers\PluginKeywordController;
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

Route::middleware('auth:sanctum')->get('/user/plugins', [PluginController::class, 'getUserPlugins']);

Route::middleware('auth:sanctum')->delete('/user/plugins/{slug}', [PluginController::class, 'destroy']);

Route::get('/plugins/{slug}', [PluginController::class, 'show']);

Route::middleware( 'auth:sanctum' )->get( '/plugin-stats/{slug}', [ PluginStatsController::class, 'download' ] );

Route::middleware('auth:sanctum')->group(function () {
    Route::get('/plugin-active-installs/{slug}', [PluginController::class, 'getActiveInstalls']);
});

Route::middleware('auth:sanctum')->post('plugin-position-movement', [PluginController::class, 'getPositionMovement']);

Route::middleware('auth:sanctum')->get('/plugin-average-position/{slug}', [PluginController::class, 'getAveragePosition']);

Route::middleware('auth:sanctum')->get('/plugin-downloads/{slug}', [PluginController::class, 'getDownloads']);

Route::middleware('auth:sanctum')->get('/plugin-data/{slug}', [PluginController::class, 'getPluginData']);

Route::post('plugin-keywords', [PluginKeywordController::class, 'getKeywords']);

Route::middleware('auth:sanctum')->group(function () {
    Route::delete('/keywords', [PluginKeywordController::class, 'deleteKeywords']);
    Route::post('/keywords', [PluginKeywordController::class, 'addKeywords']);
});

Route::get('/user-keywords/{slug}', [PluginKeywordController::class, 'getUserKeywords'])
    ->middleware('auth:sanctum');

