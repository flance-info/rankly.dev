import json
import os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
from populate_plugin_stats_files import insert_plugin_stats

# Load environment variables
load_dotenv()

# Database connection parameters (reused from scraper_wordpress.py)
DB_CONNECTION = {
    'dbname': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Define the directory path
base_dir = os.path.dirname(__file__)
stats_dir = os.path.join(base_dir, "output", "stats")

def insert_plugin(conn, plugin_data):
    """Insert plugin data into the database (reused from scraper_wordpress.py)."""
    cursor = conn.cursor()
    
    try:
        sql = """
        INSERT INTO plugins (
            name, 
            slug, 
            plugin_data,
            created_at,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (slug) 
        DO UPDATE SET 
            name = EXCLUDED.name,
            plugin_data = EXCLUDED.plugin_data,
            updated_at = EXCLUDED.updated_at
        """
        
        now = datetime.now()
        
        cursor.execute(sql, (
            plugin_data.get('name', ''),
            plugin_data.get('slug', ''),
            json.dumps(plugin_data),
            now,
            now
        ))
        
        conn.commit()
      #  print(f"Successfully inserted/updated plugin in DB: {plugin_data.get('slug')}")
        
    except Exception as e:
        print(f"Error inserting plugin {plugin_data.get('slug')} to DB: {e}")
        conn.rollback()
    finally:
        cursor.close()
def process_json_files():
    """Process all JSON files in the stats directory."""
    try:
        conn = psycopg2.connect(**DB_CONNECTION)
        print("Connected to database successfully")

        total_processed = 0
        db_success = 0
        stats_success = 0

        # Get all matching files
        files = [f for f in os.listdir(stats_dir) 
                if f.startswith('processed_plugins_') and f.endswith('.json')]
        
        # Sort files by the embedded date
        files = sorted(files, key=lambda x: datetime.strptime(
            x.replace('processed_plugins_', '').replace('.json', ''), 
            '%Y-%m-%d'
        ))
        
        print("\nProcessing files in this order:")
        for f in files:
            print(f"- {f}")
        print("\nStarting processing...\n")

        for filename in files:
            # Extract date from filename (assuming format: processed_plugins_YYYY-MM-DD.json)
            try:
                stat_date = filename.replace('processed_plugins_', '').replace('.json', '')
                # Validate date format
                datetime.strptime(stat_date, '%Y-%m-%d')
            except ValueError:
                print(f"Invalid date format in filename: {filename}")
                continue

            file_path = os.path.join(stats_dir, filename)
            print(f"\nProcessing file: {filename} for date: {stat_date}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    plugins = json.load(file)
                    
                    for plugin in plugins:
                        total_processed += 1
                        
                        try:
                            # Insert/update plugin data
                            insert_plugin(conn, plugin)
                            db_success += 1

                            # Add stat_date to plugin data
                            plugin['stat_date'] = stat_date
                            # Insert plugin stats with the file date
                            insert_plugin_stats(conn, plugin)
                            stats_success += 1
                            
                            print(f"\rProcessed: {total_processed} | "
                                  f"DB Success: {db_success} | "
                                  f"Stats Success: {stats_success}", end="")
                            
                        except Exception as e:
                            print(f"\nError processing plugin {plugin.get('slug')}: {e}")

            except json.JSONDecodeError as e:
                print(f"Error reading JSON file {filename}: {e}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

        print("\n\n=== Final Summary ===")
        print(f"Total plugins processed: {total_processed}")
        print(f"Successfully saved to database: {db_success}")
        print(f"Successfully saved stats: {stats_success}")

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed")
if __name__ == "__main__":
    process_json_files()