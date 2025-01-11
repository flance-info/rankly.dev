import os
import subprocess
import time
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_size(env, db_name, db_user, db_host):
    """Get the total database size in bytes"""
    try:
        command = [
            'psql',
            '-h', db_host,
            '-U', db_user,
            '-d', db_name,
            '-t',  # tuple only output
            '-c', "SELECT pg_database_size(current_database());"
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        output, _ = process.communicate()
        return int(output.decode().strip())
    except:
        return None

def get_database_stats(env, db_name, db_user, db_host):
    """Get detailed database statistics"""
    try:
        command = [
            'psql',
            '-h', db_host,
            '-U', db_user,
            '-d', db_name,
            '-t',  # tuple only output
            '-c', """
                SELECT 
                    sum(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename))),
                    sum(n_live_tup)
                FROM pg_tables
                JOIN pg_stat_user_tables 
                    ON tablename = relname
                WHERE schemaname = 'public';
            """
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        output, _ = process.communicate()
        size, rows = output.decode().strip().split('|')
        return int(size), int(rows)
    except:
        return None, None

def export_database():
    print("\n🚀 Starting database export process...")
    
    # Database connection details
    print("📝 Loading database configuration...")
    DB_NAME = os.getenv('DB_DATABASE', 'laravel')
    DB_USER = os.getenv('DB_USERNAME', 'laravel')
    DB_HOST = os.getenv('DB_HOST', 'db')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')
    
    print(f"📊 Database: {DB_NAME}")
    print(f"👤 User: {DB_USER}")
    print(f"🖥️  Host: {DB_HOST}")
    
    # Create dumps directory if it doesn't exist
    dumps_dir = os.path.join(os.path.dirname(__file__), '..', 'dumps')
    os.makedirs(dumps_dir, exist_ok=True)
    print(f"📁 Dumps directory: {dumps_dir}")
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"database_backup_{timestamp}.sql"
    filepath = os.path.join(dumps_dir, filename)
    print(f"📄 Creating backup file: {filename}")
    
    # Set password in environment
    env = os.environ.copy()
    env['PGPASSWORD'] = DB_PASSWORD
    
    # Get detailed database statistics
    print("\n📊 Analyzing database...")
    total_size, total_rows = get_database_stats(env, DB_NAME, DB_USER, DB_HOST)
    if total_size and total_rows:
        print(f"💾 Total database size: {total_size / (1024*1024):.2f} MB")
        print(f"📋 Total rows to export: {total_rows:,}")
        
        # Get row count per table for more detailed progress
        command = [
            'psql',
            '-h', DB_HOST,
            '-U', DB_USER,
            '-d', DB_NAME,
            '-t',
            '-c', """
                SELECT tablename, n_live_tup 
                FROM pg_stat_user_tables 
                WHERE schemaname = 'public'
                ORDER BY n_live_tup DESC;
            """
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        output, _ = process.communicate()
        tables = []
        for line in output.decode().strip().split('\n'):
            if line.strip():
                table, rows = line.split('|')
                tables.append((table.strip(), int(rows)))
        
        if tables:
            print("\n📊 Largest tables:")
            for table, rows in tables[:5]:  # Show top 5 tables
                print(f"  - {table}: {rows:,} rows")
    
    # Construct the pg_dump command
    command = [
        'pg_dump',
        '-h', DB_HOST,
        '-U', DB_USER,
        '-d', DB_NAME,
        '--clean'  # Add --clean option to drop objects before recreating
    ]
    
    print("\n⏳ Exporting database...")
    try:
        # Execute pg_dump and save to file
        with open(filepath, 'w') as f:
            process = subprocess.Popen(
                command, 
                stdout=f, 
                stderr=subprocess.PIPE,
                env=env
            )
            
            # Monitor progress
            last_size = 0
            start_time = time.time()
            while process.poll() is None:
                current_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
                if current_size != last_size:
                    elapsed_time = time.time() - start_time
                    speed = current_size / (1024*1024) / elapsed_time  # MB/s
                    
                    if total_size:
                        # Calculate progress based on typical compression ratios per table
                        estimated_final_size = total_size * 0.3  # Approximate compression
                        progress = min(100, (current_size / estimated_final_size) * 100)
                        
                        # Estimate time remaining
                        if progress > 0:
                            total_time = elapsed_time * (100 / progress)
                            remaining_time = total_time - elapsed_time
                            
                            sys.stdout.write(
                                f"\r💫 Progress: {progress:.1f}% | "
                                f"Size: {current_size / (1024*1024):.1f} MB | "
                                f"Speed: {speed:.1f} MB/s | "
                                f"ETA: {remaining_time/60:.1f} min"
                            )
                    else:
                        sys.stdout.write(
                            f"\r💫 Exported: {current_size / (1024*1024):.1f} MB | "
                            f"Speed: {speed:.1f} MB/s"
                        )
                    
                    sys.stdout.flush()
                    last_size = current_size
                time.sleep(0.1)
            
            _, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"\n❌ Error during export: {stderr.decode()}")
                return False
                
        # Get final file size
        file_size = os.path.getsize(filepath)
        file_size_mb = file_size / (1024 * 1024)  # Convert to MB
        
        print("\n\n✅ Export completed successfully!")
        print(f"📦 Final file size: {file_size_mb:.2f} MB")
        print(f"📍 Location: {filepath}")
        return True
        
    except Exception as e:
        print(f"\n❌ Export failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🗄️  Database Export Tool")
    print("=" * 50)
    
    success = export_database()
    
    print("\n" + "=" * 50)
    if success:
        print("✨ Export process completed successfully!")
    else:
        print("❌ Export process failed!")
    print("=" * 50 + "\n")