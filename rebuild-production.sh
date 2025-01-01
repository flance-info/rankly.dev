#!/bin/bash
echo "Starting Docker cleanup process..."

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null

# Remove all containers
echo "Removing all containers..."
docker container prune -f

# Remove all unused images
echo "Removing unused Docker images..."
docker image prune -a -f

# Remove all unused volumes
echo "Removing unused Docker volumes..."
docker volume prune -f

# Remove all unused networks
echo "Removing unused Docker networks..."
docker network prune -f

# Remove Docker build cache
echo "Cleaning Docker build cache..."
docker builder prune -f

# Optional: Completely remove all Docker resources (comment this if not needed)
# echo "Performing a full Docker cleanup (all resources)..."
# docker system prune -a --volumes -f

# Check disk space usage
echo "Docker disk usage after cleanup:"
docker system df

echo "Cleanup completed!"
set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Ensures that pipeline returns the exit status of the last command to fail



echo "🔄 Stopping all containers..."
docker-compose down

echo "🗑️ Cleaning up directories..."
# Uncomment if you want to remove node_modules
rm -rf node_modules/
rm -rf public/build/

echo "🏗️ Rebuilding containers without cache..."
docker-compose build --no-cache

echo "📦 Starting node service..."
docker-compose up -d node

echo "⚙️ Installing npm dependencies..."
docker-compose exec node npm install

echo "🔨 Building assets for production..."
docker-compose exec node npm run build


echo "🔍 Verifying contents of build directory in node container..."
docker-compose exec node ls -la /app/public/build/

echo "📂 Copying build files from node container..."
docker cp $(docker-compose ps -q node):/app/public/build ./public/

echo "🔍 Checking if files were copied to public/build..."
if [ -d "public/build" ] && [ "$(ls -A public/build)" ]; then
    echo "✅ Build files successfully copied to public/build:"
    ls -la public/build/
else
    echo "❌ Build files were not copied to public/build. Exiting."
    exit 1
fi

echo "🔐 Setting permissions..."
chmod -R 755 public/build
docker-compose exec app chown -R www-data:www-data public/build

echo "⏹️ Stopping node service..."
docker-compose stop node

echo "🚀 Starting all services..."
docker-compose up -d

echo "🧹 Clearing Laravel caches..."
docker-compose exec app php artisan cache:clear
docker-compose exec app php artisan config:clear
docker-compose exec app php artisan view:clear
docker-compose exec app php artisan route:clear

echo "✅ Rebuild complete! Checking environment..."
docker-compose exec app php artisan env 