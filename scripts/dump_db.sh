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
DB_SIZE=$(docker exec laravel-db psql -U laravel -d laravel -c "SELECT pg_size_pretty(pg_database_size('laravel'));" -t | tr -d ' ')

echo -e "${GREEN}Database size estimate: ${DB_SIZE}${NC}"

# Execute pg_dump inside the database container with progress and pipe directly to rclone
echo -e "${GREEN}[$(date +%H:%M:%S)] Creating database dump and uploading simultaneously...${NC}"

docker exec laravel-db pg_dump -U laravel laravel \
    | pv -s $(docker exec laravel-db psql -U laravel -d laravel -c "SELECT pg_database_size('laravel');" -t | tr -d ' ') \
    | gzip \
    | rclone rcat "stylemixrusty:/rankly_backups/${DUMP_FILE}" --progress

if [ $? -eq 0 ]; then
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${GREEN}Dump and upload completed successfully!${NC}"
else
    echo -e "${RED}Error: Dump and upload process failed!${NC}"
    exit 1
fi
