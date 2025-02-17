#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# SQL file to import
SQL_FILE="laravel_db_20250211_070446.sql.gz"

echo -e "${BLUE}Starting database import process...${NC}"
echo -e "${BLUE}Input file: ${NC}${SQL_FILE}"
echo -e "${BLUE}----------------------------------------${NC}"

# Get the size of the compressed file for progress bar
FILE_SIZE=$(gzip -l ${SQL_FILE} | tail -1 | awk '{print $2}')

# Import the database with progress bar
echo -e "${GREEN}[$(date +%H:%M:%S)] Importing database...${NC}"

gunzip -c ${SQL_FILE} | \
pv -s ${FILE_SIZE} | \
docker exec -i laravel-live-latest psql -U laravel -d laravel

if [ $? -eq 0 ]; then
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${GREEN}Database import completed successfully!${NC}"
else
    echo -e "${RED}Error: Database import failed!${NC}"
    exit 1
fi
