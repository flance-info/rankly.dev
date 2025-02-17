#!/usr/bin/env python3

import subprocess
import sys
import os
from tqdm import tqdm
import gzip
import glob
from datetime import datetime

# Colors for output
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def print_colored(color, message):
    print(f"{color}{message}{NC}")

def get_uncompressed_size(gz_file):
    with gzip.open(gz_file, 'rb') as f:
        f.seek(-4, 2)  # Seek to 4 bytes from end
        return int.from_bytes(f.read(), 'little')

def import_sql():
    # Get the backup directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(script_dir, "..", "storage", "app", "backup")
    
    # Find the latest SQL backup file
    sql_files = glob.glob(os.path.join(backup_dir, "laravel_db_*.sql.gz"))
    if not sql_files:
        print(f"Error: No SQL backup files found in {backup_dir}")
        return False
    
    latest_sql = max(sql_files, key=os.path.getctime)
    if not os.path.exists(latest_sql):
        print(f"Error: SQL file not found at {latest_sql}")
        return False

    print(f"Importing {os.path.basename(latest_sql)}...")
    
    try:
        # Use gunzip to decompress and pipe to psql
        process = subprocess.Popen(
            f'gunzip -c "{latest_sql}" | docker exec -i rankly-postgres-1 psql -U postgres -d rankly',
            shell=True
        )
        process.wait()
        
        if process.returncode == 0:
            print("Database import completed successfully!")
            return True
        else:
            print("Error: Database import failed!")
            return False
            
    except Exception as e:
        print(f"Error during import: {str(e)}")
        return False

if __name__ == "__main__":
    import_sql()
