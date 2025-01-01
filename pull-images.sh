#!/bin/bash

# Docker Hub credentials
DOCKER_USERNAME="elcana100"
DOCKER_TOKEN="dckr_pat_Fb6BC_w-NAhqqGT6QU8EVnh4_yc"

# Login to Docker Hub
echo "Logging into Docker Hub as $DOCKER_USERNAME..."
echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USERNAME" --password-stdin
if [ $? -ne 0 ]; then
  echo "Docker login failed. Exiting."
  exit 1
fi
echo "Login successful!"

# List of Docker images to pull
IMAGES=(
    "elcana100/laravel-app:latest"
    "elcana100/node-app:latest"
    "elcana100/rankly-node:latest"
    "elcana100/pgadmin:latest"
    "elcana100/postgres:13"
    "elcana100/python:3.11.3"
)

# Pull each image
echo "Starting to pull Docker images..."
for IMAGE in "${IMAGES[@]}"; do
    echo "Pulling $IMAGE..."
    docker pull $IMAGE
    if [ $? -eq 0 ]; then
        echo "✓ Successfully pulled $IMAGE"
    else
        echo "✗ Failed to pull $IMAGE"
    fi
done

# Summary
echo ""
echo "=== Pull Summary ==="
echo "All images processed!"
