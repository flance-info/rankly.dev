import psycopg2
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_db():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_DATABASE', 'rankly-db1'),
            user=os.getenv('DB_USERNAME', 'laravel'),
            password=os.getenv('DB_PASSWORD', 'secret'),
            host=os.getenv('DB_HOST', 'db'),
            port=os.getenv('DB_PORT', '5432')
        )
        conn.autocommit = True  # VACUUM FULL needs to run outside a transaction
        return conn
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")
        return None

def get_table_size(cursor, table_name):
    """Get the size of a table in bytes."""
    cursor.execute(f"SELECT pg_total_relation_size('{table_name}');")
    return cursor.fetchone()[0]

def vacuum_full_with_real_progress():
    """Run VACUUM FULL on plugin_keyword_stats with real progress display."""
    conn = connect_db()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            # Get the table size before VACUUM FULL
            initial_size = get_table_size(cursor, 'plugin_keyword_stats')
            print(f"📊 Table size before VACUUM FULL: {initial_size / (1024 * 1024):.2f} MB")

            # Start VACUUM FULL in a separate thread
            print("🚀 Running VACUUM FULL on plugin_keyword_stats...")
            start_time = time.time()

            # Execute VACUUM FULL in a separate thread
            cursor.execute("VACUUM FULL plugin_keyword_stats;")

            # Monitor progress by checking table size changes
            with tqdm(total=initial_size, desc="Progress", unit="B", unit_scale=True) as pbar:
                while True:
                    current_size = get_table_size(cursor, 'plugin_keyword_stats')
                    pbar.update(initial_size - current_size)
                    if current_size >= initial_size:
                        break
                    time.sleep(1)  # Check progress every second

            # Get the table size after VACUUM FULL
            final_size = get_table_size(cursor, 'plugin_keyword_stats')
            print(f"📊 Table size after VACUUM FULL: {final_size / (1024 * 1024):.2f} MB")
            print(f"⏱️  Total time: {time.time() - start_time:.2f} seconds")

    except Exception as e:
        print(f"❌ Error during VACUUM FULL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    vacuum_full_with_real_progress() 