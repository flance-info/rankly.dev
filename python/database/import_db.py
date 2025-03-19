import os
import subprocess
import argparse
import time
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_file_size(filepath):
    """Get the size of the SQL file"""
    try:
        return os.path.getsize(filepath)
    except:
        return None

def list_backup_files():
    """List all available backup files with details"""
    dumps_dir = os.path.join(os.path.dirname(__file__), '..', 'dumps')
    
    if not os.path.exists(dumps_dir):
        print("❌ Dumps directory not found!")
        return []
    
    # Get all SQL files and sort by modification time
    files = []
    for f in os.listdir(dumps_dir):
        if f.endswith('.sql'):
            path = os.path.join(dumps_dir, f)
            size = os.path.getsize(path)
            mtime = os.path.getmtime(path)
            files.append({
                'name': f,
                'size': size,
                'mtime': mtime,
                'path': path
            })
    
    # Sort files by modification time (newest first)
    files.sort(key=lambda x: x['mtime'], reverse=True)
    return files

def print_backup_list(files):
    """Print the list of backup files in a formatted way"""
    if not files:
        print("❌ No backup files found!")
        return None
    
    print("\n📁 Available backup files:")
    print("=" * 80)
    print(f"{'#':<4} {'Filename':<40} {'Size':>10} {'Date':>24}")
    print("-" * 80)
    
    for i, file in enumerate(files, 1):
        size_mb = file['size'] / (1024 * 1024)
        date = datetime.fromtimestamp(file['mtime']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{i:<4} {file['name']:<40} {f'{size_mb:.2f} MB':>10} {date:>24}")
    
    print("=" * 80)
    return True

def select_backup_file(files):
    """Let user select which file to import"""
    while True:
        try:
            choice = input("\n📎 Enter the number of the file to import (or 'q' to quit): ")
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(files):
                return files[index]['name']
            else:
                print("❌ Invalid number! Please try again.")
        except ValueError:
            print("❌ Please enter a valid number!")

def import_database(filename):
    print("\n🚀 Starting database import process...")
    
    # Database connection details
    print("📝 Loading database configuration...")
    DB_NAME = os.getenv('DB_DATABASE', 'laravel')
    DB_USER = os.getenv('DB_USERNAME', 'laravel')
    DB_HOST = os.getenv('DB_HOST', 'db')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')
    
    print(f"📊 Database: {DB_NAME}")
    print(f"👤 User: {DB_USER}")
    print(f"🖥️  Host: {DB_HOST}")
    
    # Construct full path to dump file
    dumps_dir = os.path.join(os.path.dirname(__file__), '..', 'dumps')
    filepath = os.path.join(dumps_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ Error: File not found: {filepath}")
        return False
    
    # Get file size
    total_size = get_file_size(filepath)
    if total_size:
        print(f"📦 Import file size: {total_size / (1024*1024):.2f} MB")
    
    # Set password in environment
    env = os.environ.copy()
    env['PGPASSWORD'] = DB_PASSWORD
    
    # Construct the psql command
    command = [
        'psql',
        '-h', DB_HOST,
        '-U', DB_USER,
        '-d', DB_NAME
    ]
    
    print("\n⏳ Importing database...")
    try:
        # Execute psql with the dump file
        with open(filepath, 'r') as f:
            process = subprocess.Popen(
                command,
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            # Monitor progress
            start_time = time.time()
            last_position = 0
            
            while process.poll() is None:
                current_position = f.tell()
                if current_position != last_position:
                    elapsed_time = time.time() - start_time
                    speed = current_position / (1024*1024) / elapsed_time  # MB/s
                    
                    if total_size:
                        progress = min(100, (current_position / total_size) * 100)
                        remaining_time = (total_size - current_position) / (speed * 1024*1024) if speed > 0 else 0
                        
                        sys.stdout.write(
                            f"\r💫 Progress: {progress:.1f}% | "
                            f"Processed: {current_position / (1024*1024):.1f} MB | "
                            f"Speed: {speed:.1f} MB/s | "
                            f"ETA: {remaining_time/60:.1f} min"
                        )
                    else:
                        sys.stdout.write(
                            f"\r💫 Processed: {current_position / (1024*1024):.1f} MB | "
                            f"Speed: {speed:.1f} MB/s"
                        )
                    
                    sys.stdout.flush()
                    last_position = current_position
                time.sleep(0.1)
            
            _, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"\n❌ Error during import: {stderr.decode()}")
                return False
                
        print("\n\n✅ Import completed successfully!")
        print(f"⏱️  Total time: {(time.time() - start_time)/60:.1f} minutes")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🗄️  Database Import Tool")
    print("=" * 50)
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Import database from SQL dump file')
    parser.add_argument('filename', nargs='?', help='Optional: Name of the SQL dump file')
    args = parser.parse_args()
    
    # List available backup files
    files = list_backup_files()
    
    if args.filename:
        # Direct import with provided filename
        filename = args.filename
        print(f"\n📦 Selected file: {filename}")
    else:
        # Interactive mode
        if print_backup_list(files):
            filename = select_backup_file(files)
        else:
            sys.exit(1)
    
    if filename:
        proceed = input("⚠️  Do you want to proceed with the import? (y/N): ")
        
        if proceed.lower() == 'y':
            success = import_database(filename)
            
            print("\n" + "=" * 50)
            if success:
                print("✨ Import process completed successfully!")
            else:
                print("❌ Import process failed!")
            print("=" * 50 + "\n")
        else:
            print("\n🛑 Import cancelled by user.")
    else:
        print("\n🛑 No file selected. Import cancelled.") 