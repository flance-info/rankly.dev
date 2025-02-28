#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DUMP_FILE="laravel_db_${TIMESTAMP}.sql.gz"
DUMP_FILE_PATH="/app/dumps/${DUMP_FILE}"

# Start dump with progress
echo -e "${BLUE}Starting database dump and upload process...${NC}"
echo -e "${BLUE}Output file: ${NC}$DUMP_FILE"
echo -e "${BLUE}----------------------------------------${NC}"

# Create dumps directory in the app container
docker exec laravel-app mkdir -p /app/dumps

# Get an estimated database size
DB_SIZE=$(docker exec laravel-db-timescale psql -U laravel -d laravel -c "SELECT pg_size_pretty(pg_database_size('laravel'));" -t | tr -d ' ')

echo -e "${GREEN}Database size estimate: ${DB_SIZE}${NC}"

# Function to upload with retries and exponential backoff
upload_with_backoff() {
    local retry_count=0
    local max_retries=5
    local delay=1

    while [ $retry_count -lt $max_retries ]; do
        echo -e "${GREEN}[$(date +%H:%M:%S)] Creating database dump and uploading simultaneously...${NC}"

        docker exec laravel-db-timescale pg_dump -U laravel laravel \
            | pv -s $(docker exec laravel-db-timescale psql -U laravel -d laravel -c "SELECT pg_database_size('laravel');" -t | tr -d ' ') \
            | gzip \
            | rclone rcat "stylemixrusty:/rankly_backups/${DUMP_FILE}" --progress

        if [ $? -eq 0 ]; then
            echo -e "${BLUE}----------------------------------------${NC}"
            echo -e "${GREEN}Dump and upload completed successfully!${NC}"
            return 0
        else
            retry_count=$((retry_count + 1))
            echo -e "${RED}Error: Upload failed. Retrying in ${delay} seconds... (Attempt ${retry_count}/${max_retries})${NC}"
            sleep $delay
            delay=$((delay * 2))  # Exponential backoff
        fi
    done

    echo -e "${RED}Error: Dump and upload process failed after ${max_retries} attempts!${NC}"
    exit 1
}

# Call the upload function
upload_with_backoff
