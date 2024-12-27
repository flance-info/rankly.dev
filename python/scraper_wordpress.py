import json
import requests
import os
from datetime import datetime
from threading import Lock
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_CONNECTION = {
    'dbname': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

base_dir = os.path.dirname(__file__)
output_dir = os.path.join(base_dir, "output", "stats")

# Create the directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# WordPress Plugin API Base URL
PLUGIN_API_BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"

# Lock for thread-safe file operations
file_lock = Lock()

def insert_plugin(conn, plugin_data):
    """Insert plugin data into the database."""
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
        print(f"Successfully inserted/updated plugin in DB: {plugin_data.get('slug')}")
        
    except Exception as e:
        print(f"Error inserting plugin {plugin_data.get('slug')} to DB: {e}")
        conn.rollback()
    finally:
        cursor.close()

def get_total_pages(per_page):
    """Fetch the total number of pages from the WordPress Plugin API."""
    params = {
        "action": "query_plugins",
        "request[fields][name]": True,
        "request[page]": 1,
        "request[per_page]": per_page  
    }
    try:
        response = requests.get(PLUGIN_API_BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            info = data.get('info', {})
            return info.get('pages', 1)
        else:
            print(f"Failed to fetch total pages: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching total pages: {e}")
    return 1

def get_plugins_list():
    """Fetch a list of plugins from the WordPress API and filter fields."""
    all_plugins = []
    per_page = 200
    total_pages = get_total_pages(per_page)
    total_plugins_processed = 0
    db_success_count = 0
    file_success_count = 0
   
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONNECTION)
        print("Connected to database successfully")

        for page in range(1, total_pages + 1):
            params = {
                "action": "query_plugins",
                "request[page]": page,
                "request[per_page]": per_page
            }
            try:
                response = requests.get(PLUGIN_API_BASE_URL, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    plugins = data.get('plugins', [])
                    page_plugin_count = len(plugins)

                    print(f"\nProcessing page {page}/{total_pages} ({page_plugin_count} plugins)")
                    
                    # Process each plugin
                    for index, plugin in enumerate(plugins, 1):
                        plugin_name = plugin.get('name', '')
                        plugin_slug = plugin.get('slug', '')
                        
                        # Create filtered version for file storage
                        filtered_plugin = {
                            "name": plugin_name,
                            "slug": plugin_slug,
                            "rating": plugin.get("rating"),
                            "ratings": plugin.get("ratings"),
                            "num_ratings": plugin.get("num_ratings"),
                            "active_installs": plugin.get("active_installs"),
                            "last_updated": plugin.get("last_updated"),
                            "added": plugin.get("added"),
                            "tags": plugin.get("tags")
                        }
                        
                        # Store filtered data for file
                        all_plugins.append(filtered_plugin)
                        file_success_count += 1
                        print(f"\n📁 Added to file queue: {plugin_name} ({plugin_slug})")
                        
                        # Store complete data in DB
                        try:
                            insert_plugin(conn, plugin)
                            db_success_count += 1
                            print(f"💾 Saved to database: {plugin_name} ({plugin_slug})")
                        except Exception as e:
                            print(f"❌ Database error for {plugin_name}: {str(e)}")
                        
                        total_plugins_processed += 1
                        
                        # Display progress summary
                        print(f"\rProgress: {index}/{page_plugin_count} on page | "
                              f"Total: {total_plugins_processed} | "
                              f"DB: {db_success_count} | "
                              f"File Queue: {file_success_count}", end="\n")
                    
                    print(f"\nCompleted page {page}/{total_pages}")
                    print(f"Database saves: {db_success_count}")
                    print(f"File queue additions: {file_success_count}")
                    print(f"Total processed: {total_plugins_processed}")
                    
                else:
                    print(f"Failed to fetch plugins list: {response.status_code}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"Error fetching plugins list: {e}")
                break

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("\n=== Final Summary ===")
            print(f"Total plugins processed: {total_plugins_processed}")
            print(f"Successfully saved to database: {db_success_count}")
            print(f"Added to file queue: {file_success_count}")
            print("Database connection closed")

    return all_plugins

def batch_save_to_file(data_batch, file_path):
    """Batch save processed data to a JSON file in a thread-safe manner."""
    with file_lock:
        try:
            if os.path.exists(file_path):
                with open(file_path, "r+", encoding="utf-8") as file:
                    try:
                        existing_data = json.load(file)
                    except json.JSONDecodeError:
                        existing_data = []

                    existing_data.extend(data_batch)
                    file.seek(0)
                    json.dump(existing_data, file, ensure_ascii=False, indent=4)
            else:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data_batch, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data to file: {e}")

def process_plugins():
    """Process plugins and save their info."""
    output_file = os.path.join(output_dir, f"processed_plugins_{datetime.now().strftime('%Y-%m-%d')}.json")

    # Fetch plugins list
    plugins = get_plugins_list()
    print(f"Total plugins fetched: {len(plugins)}")

    # Save plugins data to file
    if plugins:
        batch_save_to_file(plugins, output_file)
        print(f"Saved {len(plugins)} plugins to file.")

if __name__ == "__main__":
    process_plugins()