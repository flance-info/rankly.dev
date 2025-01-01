#!/bin/bash

echo "🔍 Checking Vite Base Configuration..."

# Check vite.config.js base configuration
echo "📄 Vite Base URL Configuration:"
docker-compose exec app grep -A 5 "base:" /app/vite.config.js

# Check Laravel asset URL configuration
echo -e "\n🌐 Asset URL Configuration:"
docker-compose exec app grep "ASSET_URL" /app/.env

# Check Vite server configuration
echo -e "\n⚙️ Vite Server Configuration:"
docker-compose exec app grep -A 10 "server:" /app/vite.config.js

# Check if manifest exists and its URLs
echo -e "\n📝 Manifest URLs (if exists):"
docker-compose exec app cat /app/public/build/manifest.json 2>/dev/null | grep "url"

echo -e "\n✅ Vite base configuration check complete!" 