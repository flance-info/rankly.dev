import json
from collections import Counter

# Path to the JSON file
file_path = r"D:\domains\rankly\python\plugins_all_pages.json"

def find_duplicates(file_path):
    """Find duplicate plugins in the JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            
            if not isinstance(data, list):
                print("Invalid data format. Expected a list.")
                return

            # Extract names and links
            names = [plugin['Name'] for plugin in data]
            links = [plugin['Link'] for plugin in data]

            # Find duplicates in names and links
            duplicate_names = [name for name, count in Counter(names).items() if count > 1]
            duplicate_links = [link for link, count in Counter(links).items() if count > 1]

            # Display duplicates
            if duplicate_names:
                print(f"Duplicate Names ({len(duplicate_names)} found):")
                for name in duplicate_names:
                    print(f"  - {name}")
            else:
                print("No duplicate names found.")
            
            if duplicate_links:
                print(f"Duplicate Links ({len(duplicate_links)} found):")
                for link in duplicate_links:
                    print(f"  - {link}")
            else:
                print("No duplicate links found.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    find_duplicates(file_path)
