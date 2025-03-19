import json
import os

# Base directory for the output files
base_dir = os.path.dirname(__file__)

# Path to the processed plugins file
processed_plugins_file = os.path.join(base_dir, "output", "processed_plugins_2024-12-12.json")

# Path to the output tags file
tags_file = os.path.join(base_dir, "output", "tags.json")

def extract_tags_from_plugins(file_path):
    """Extract unique tags from the processed plugins file."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            plugins = json.load(file)
            tags = {}

            for plugin in plugins:
                plugin_tags = plugin.get("tags", {})
                if isinstance(plugin_tags, dict):
                    for slug, label in plugin_tags.items():
                        if slug not in tags:
                            tags[slug] = label

            return [{"slug": slug, "label": label} for slug, label in tags.items()]
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return []

def save_tags_to_file(tags, file_path):
    """Save unique tags to a JSON file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(tags, file, ensure_ascii=False, indent=4)
        print(f"Tags saved to {file_path}")
    except Exception as e:
        print(f"Error saving tags to file: {e}")

if __name__ == "__main__":
    # Extract tags from the processed plugins file
    unique_tags = extract_tags_from_plugins(processed_plugins_file)

    # Save the unique tags to a file
    save_tags_to_file(unique_tags, tags_file)