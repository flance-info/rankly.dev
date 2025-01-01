#!/bin/bash

echo "🔄 Stopping containers..."
docker-compose down

echo "📦 Starting node service..."
docker-compose up -d node

echo "🔨 Building assets..."
docker-compose exec node npm run build

echo "📂 Copying build files..."
docker cp $(docker-compose ps -q node):/app/public/build ./public/

echo "🔐 Setting permissions..."
chmod -R 755 public/build
docker-compose exec app chown -R www-data:www-data public/build

echo "⏹️ Stopping node service..."
docker-compose stop node

echo "🚀 Starting all services..."
docker-compose up -d

echo "✅ Build complete!" 