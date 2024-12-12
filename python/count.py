import json

# Path to the JSON file
file_path = r"D:\domains\rankly\python\plugins_all_pages.json"

def count_plugins(file_path):
    """Count the number of plugins in the JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                print(f"Total number of plugins: {len(data)}")
            else:
                print("Invalid data format. Expected a list.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    count_plugins(file_path)
