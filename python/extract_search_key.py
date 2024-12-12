import json
import os
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict
from asyncio import Semaphore
import time
from datetime import timedelta

# Base directory for the output files
base_dir = os.path.dirname(__file__)

# Path to the tags file
tags_file = os.path.join(base_dir, "output", "tags.json")

# WordPress Plugin API Base URL
PLUGIN_API_BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"

def load_tags(file_path):
    """Load tags from the JSON file."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return []

async def search_plugins_by_tag_page(session: aiohttp.ClientSession, tag_label: str, page: int, sem: Semaphore) -> tuple[int, List[Dict]]:
    """Fetch a single page of plugins asynchronously."""
    params = {
        "action": "query_plugins",
        "search": tag_label,
        "page": page,
        "per_page": 200
    }
    
    async with sem:  # Limit concurrent requests
        try:
            # Add delay between requests (1 second per request)
            await asyncio.sleep(1)  # Slightly more than 1 second to be safe
            
            async with session.get(PLUGIN_API_BASE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Fetched page {page} for tag '{tag_label}'")
                    return page, data.get('plugins', [])
                elif response.status == 429:
                    print(f"Rate limit hit for page {page} tag '{tag_label}', retrying after delay...")
                    await asyncio.sleep(30)  # Wait a full minute before retry
                    # Retry the request
                    async with session.get(PLUGIN_API_BASE_URL, params=params) as retry_response:
                        if retry_response.status == 200:
                            data = await retry_response.json()
                            print(f"Successfully retried page {page} for tag '{tag_label}'")
                            return page, data.get('plugins', [])
                        else:
                            print(f"Failed retry for page {page} tag '{tag_label}': {retry_response.status}")
                            return page, []
                else:
                    print(f"Failed to fetch page {page} for tag '{tag_label}': {response.status}")
                    return page, []
        except Exception as e:
            print(f"Error fetching page {page} for tag '{tag_label}': {e}")
            return page, []

async def search_plugins_by_tag(session: aiohttp.ClientSession, tag_label: str, sem: Semaphore) -> List[Dict]:
    """Search for plugins using the WordPress API by tag label asynchronously."""
    params = {
        "action": "query_plugins",
        "search": tag_label,
        "page": 1,
        "per_page": 200
    }
    
    try:
        async with sem:
            async with session.get(PLUGIN_API_BASE_URL, params=params) as response:
                if response.status != 200:
                    print(f"Failed to fetch initial data for tag '{tag_label}'")
                    return []
                
                data = await response.json()
                total_pages = data.get('info', {}).get('pages', 1)
                all_plugins = data.get('plugins', [])  # First page plugins
                
                if total_pages <= 1:
                    return all_plugins
                
                # Create tasks for remaining pages
                tasks = [
                    search_plugins_by_tag_page(session, tag_label, page, sem)
                    for page in range(2, total_pages + 1)
                ]
                
                # Gather results
                results = await asyncio.gather(*tasks)
                
                # Sort results by page number and combine plugins
                sorted_results = sorted(results, key=lambda x: x[0])
                for _, plugins in sorted_results:
                    all_plugins.extend(plugins)
                
                return all_plugins
                
    except Exception as e:
        print(f"Error in search_plugins_by_tag for '{tag_label}': {e}")
        return []

async def process_single_tag(session: aiohttp.ClientSession, tag: Dict, request_sem: Semaphore, tag_sem: Semaphore):
    """Process a single tag."""
    async with tag_sem:  # Limit concurrent tag processing
        tag_label_to_search = tag['label']
        tag_slug = tag['slug']
        
        start_time = time.time()
        print(f"\nStarting tag: {tag_label_to_search}")
        
        plugins = await search_plugins_by_tag(session, tag_label_to_search, request_sem)
        
        elapsed_time = time.time() - start_time
        elapsed_formatted = str(timedelta(seconds=int(elapsed_time)))
        print(f"Completed tag '{tag_label_to_search}' in {elapsed_formatted}")
        print(f"Found {len(plugins)} plugins for tag '{tag_label_to_search}'")
        
        if plugins:
            save_results_to_file(plugins, tag_slug, tag_label_to_search)
        else:
            print(f"No plugins found for tag '{tag_label_to_search}'")

async def process_tags(tags: List[Dict]):
    """Process multiple tags concurrently."""
    start_time = time.time()
    print(f"Starting processing of {len(tags)} tags at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    request_sem = Semaphore(5)
    tag_sem = Semaphore(1)
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            process_single_tag(session, tag, request_sem, tag_sem)
            for tag in tags
        ]
        await asyncio.gather(*tasks)
    
    elapsed_time = time.time() - start_time
    elapsed_formatted = str(timedelta(seconds=int(elapsed_time)))
    print(f"\nTotal processing time: {elapsed_formatted}")

def save_results_to_file(plugins, tag_slug, tag_label):
    """Save search results to a file named with the tag slug and current date."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(base_dir, "output", "keywords", tag_slug)
    file_name = f"{tag_slug}_plugins_{current_date}.json"
    file_path = os.path.join(folder_path, file_name)

    # Ensure the directory exists
    os.makedirs(folder_path, exist_ok=True)

    # Prepare data with tag information and plugins
    output_data = {
        "tag_slug": tag_slug,
        "tag_label": tag_label,
        "plugins": [{"order": i + 1, "slug": plugin["slug"], "name": plugin["name"]} for i, plugin in enumerate(plugins)]
    }

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(output_data, file, ensure_ascii=False, indent=4)
        print(f"Results saved to {file_path}")
    except Exception as e:
        print(f"Error saving results to file: {e}")

if __name__ == "__main__":
    # Load tags from the tags file
    tags = load_tags(tags_file)

    
    test_tags = tags[:30]
    
    # Run the async process
    asyncio.run(process_tags(test_tags)) 