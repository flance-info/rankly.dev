#!/bin/bash

echo "🔍 Checking Vite Configuration..."

# Check vite.config.js content
echo "📄 vite.config.js content:"
docker-compose exec app cat /app/vite.config.js

# Check environment variables related to Vite
echo -e "\n🌍 Vite Environment Variables:"
docker-compose exec app env | grep VITE

# Check if build directory exists and its contents
echo -e "\n📦 Build Directory Contents:"
docker-compose exec app ls -la /app/public/build

# Check manifest.json if it exists
echo -e "\n📝 Manifest Content (if exists):"
docker-compose exec app cat /app/public/build/manifest.json 2>/dev/null || echo "manifest.json not found"

echo -e "\n✅ Vite configuration check complete!" 