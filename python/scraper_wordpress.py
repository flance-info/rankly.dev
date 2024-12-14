import json
import requests
import os
from datetime import datetime
from threading import Lock


base_dir = os.path.dirname(__file__)

output_dir = os.path.join(base_dir,"output", "stats")

# Create the directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# WordPress Plugin API Base URL
PLUGIN_API_BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"

# Lock for thread-safe file operations
file_lock = Lock()

# Generate output file name with the current date
def generate_output_file():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(output_dir, f"processed_plugins_{current_date}.json")

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
    """Fetch a list of plugins from the WordPress Plugin API and filter fields."""
    all_plugins = []
    per_page = 200
    total_pages = get_total_pages(per_page)
   

    for page in range(1, total_pages + 1):
        params = {
            "action": "query_plugins",          
            "request[fields][name]": True,
            "request[fields][slug]": True,
            "request[fields][rating]": True,
            "request[fields][ratings]": True,
            "request[fields][num_ratings]": True,
            "request[fields][active_installs]": True,
            "request[fields][last_updated]": True,
            "request[fields][added]": True,
            "request[fields][tags]": True,
            "request[page]": page,
            "request[per_page]": per_page
        }
        try:
            response = requests.get(PLUGIN_API_BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                plugins = data.get('plugins', [])

                # Filter the data to include only the specified fields
                filtered_plugins = [
                    {
                        "name": plugin.get("name"),
                        "slug": plugin.get("slug"),
                        "rating": plugin.get("rating"),
                        "ratings": plugin.get("ratings"),
                        "num_ratings": plugin.get("num_ratings"),
                        "active_installs": plugin.get("active_installs"),
                        "last_updated": plugin.get("last_updated"),
                        "added": plugin.get("added"),
                        "tags": plugin.get("tags")
                    }
                    for plugin in plugins
                ]
                all_plugins.extend(filtered_plugins)
                print(f"Fetched page {page}/{total_pages}")
            else:
                print(f"Failed to fetch plugins list: {response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching plugins list: {e}")
            break
    return all_plugins

def batch_save_to_file(data_batch, file_path):
    """Batch save processed data to a JSON file in a thread-safe manner."""
    with file_lock:  # Ensure only one thread writes at a time
        try:
            if os.path.exists(file_path):
                # Handle case where the file is empty or contains invalid JSON
                with open(file_path, "r+", encoding="utf-8") as file:
                    try:
                        existing_data = json.load(file)  # Try loading existing data
                    except json.JSONDecodeError:
                        existing_data = []  # If file is empty or invalid, reset to an empty list

                    # Append new data
                    existing_data.extend(data_batch)
                    file.seek(0)  # Move to the start of the file
                    json.dump(existing_data, file, ensure_ascii=False, indent=4)
            else:
                # Create a new file
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data_batch, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data to file: {e}")

def process_plugins():
    """Process plugins and save their info."""
    output_file = generate_output_file()

    # Fetch plugins list
    plugins = get_plugins_list()
    print(f"Total plugins fetched: {len(plugins)}")

    # Save plugins data
    if plugins:
        batch_save_to_file(plugins, output_file)
        print(f"Saved {len(plugins)} plugins to file.")

if __name__ == "__main__":
    process_plugins()