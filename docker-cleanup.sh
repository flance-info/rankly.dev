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

