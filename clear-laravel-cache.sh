#!/bin/bash

echo "🧹 Clearing Laravel Caches..."

# Clear all Laravel caches
docker-compose exec app php artisan cache:clear
docker-compose exec app php artisan config:clear
docker-compose exec app php artisan route:clear
docker-compose exec app php artisan view:clear

# Clear compiled classes
docker-compose exec app php artisan clear-compiled

# Clear application cache
docker-compose exec app php artisan optimize:clear

echo "✨ All Laravel caches have been cleared!"

# Verify environment
echo "🔍 Current environment:"
docker-compose exec app php artisan env 