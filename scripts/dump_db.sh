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
echo -e "${BLUE}Starting database dump...${NC}"
echo -e "${BLUE}Output file: ${NC}$DUMP_FILE"
echo -e "${BLUE}----------------------------------------${NC}"

# Create dumps directory in the app container
docker exec laravel-app mkdir -p /app/dumps

# Get an estimated database size
DB_SIZE=$(docker exec laravel-db psql -U laravel -d laravel -c "SELECT pg_size_pretty(pg_database_size('laravel'));" -t | tr -d ' ')

echo -e "${GREEN}Database size estimate: ${DB_SIZE}${NC}"

# Execute pg_dump inside the database container with progress and gzip compression
echo -e "${GREEN}[$(date +%H:%M:%S)] Creating database dump with progress...${NC}"

docker exec laravel-db pg_dump -U laravel laravel \
    | pv -s $(docker exec laravel-db psql -U laravel -d laravel -c "SELECT pg_database_size('laravel');" -t | tr -d ' ') \
    | gzip \
    | docker exec -i laravel-app tee "$DUMP_FILE_PATH" >/dev/null

# Check if dump was successful
if docker exec laravel-app test -s "$DUMP_FILE_PATH"; then
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${GREEN}Dump completed successfully!${NC}"
    echo -e "${GREEN}File size: $(docker exec laravel-app du -h "$DUMP_FILE_PATH" | cut -f1)${NC}"

    # Use rclone to move the dump to the specified remote location
    echo -e "${BLUE}Uploading to Google Drive...${NC}"
    rclone move "/path/to/local/dumps/${DUMP_FILE}" "stylemixrusty:/rankly_backups/" --progress

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Upload completed successfully!${NC}"
    else
        echo -e "${RED}Error: Upload failed!${NC}"
    fi
else
    echo -e "${RED}Error: Dump file is empty or not created!${NC}"
    exit 1
fi
