<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title inertia>{{ config('app.name', 'Laravel') }}</title>

        <!-- Add this line to define Vite server URL -->
        

        <!-- Fonts -->
        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=figtree:400,500,600&display=swap" rel="stylesheet" />

        <!-- Scripts -->
        @routes
        @production
            @php
                // Corrected the path to manifest.json
                $manifest = json_decode(file_get_contents(public_path('build/manifest.json')), true);
            @endphp
            <script type="module" src="/build/{{ $manifest['resources/js/app.js']['file'] }}"></script>
            <!-- If you have CSS files, include them similarly -->
            @foreach($manifest['resources/js/app.js']['css'] ?? [] as $css)
                <link rel="stylesheet" href="/build/{{ $css }}">
            @endforeach
        @else
            @vite(['resources/js/app.js', "resources/js/Pages/{$page['component']}.vue"])
        @endproduction
        @inertiaHead
    </head>
    <body class="font-sans antialiased">
        @inertia
    </body>
</html>
