import json
import os
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict
from asyncio import Semaphore
import time
from datetime import timedelta
import itertools
import random

# Base directory for the output files
base_dir = os.path.dirname(__file__)

# Path to the tags file
tags_file = os.path.join(base_dir, "output", "tags.json")

# WordPress Plugin API Base URL
PLUGIN_API_BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"

# Updated list of proxies
proxies = [
    "http://198.23.239.134:6540",
    "http://207.244.217.165:6712",
    "http://107.172.163.27:6543",
    "http://64.137.42.112:5157",
    "http://173.211.0.148:6641",
    "http://161.123.152.115:6360",
    "http://167.160.180.203:6754",
    "http://154.36.110.199:6853",
    "http://173.0.9.70:5653"
]

# Create an iterator to cycle through the proxies
proxy_cycle = itertools.cycle(proxies)

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

async def check_proxy(proxy: str) -> bool:
    """Check if a proxy is working by making a request to IP-API."""
    test_url = "http://ip-api.com/json/?fields=61439"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(test_url, proxy=proxy, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Proxy {proxy} is working. IP: {data.get('query'), data.get('city')}")
                    return True
                else:
                    print(f"Proxy {proxy} failed with status: {response.status}")
                    return False
    except Exception as e:
        print(f"Error checking proxy {proxy}: {e}")
        return False

async def get_working_proxy() -> str:
    """Get a random working proxy from the list."""
    while True:
        proxy = random.choice(proxies)
        if await check_proxy(proxy):
            return proxy
        else:
            print(f"Proxy {proxy} is not working, trying another...")

def is_tag_processed(tag_slug: str) -> bool:
    """Check if the tag has already been processed for the current date."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{tag_slug}_plugins_{current_date}.json"
    file_path = os.path.join(base_dir, "output", "keywords", tag_slug, file_name)
    return os.path.exists(file_path)

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
            # Reduce delay between requests
            await asyncio.sleep(0.5)  # Try with 0.5 seconds delay
            
            # Get a working proxy
            proxy = await get_working_proxy()
            print(f"Using proxy {proxy} for page {page} of tag '{tag_label}'")
            
            async with session.get(PLUGIN_API_BASE_URL, params=params, proxy=proxy) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Fetched page {page} for tag '{tag_label}' using proxy {proxy}")
                    return page, data.get('plugins', [])
                elif response.status == 429:
                    print(f"Rate limit hit for page {page} tag '{tag_label}', retrying after delay...")
                    await asyncio.sleep(2)  # Wait a full minute before retry
                    # Retry the request
                    async with session.get(PLUGIN_API_BASE_URL, params=params, proxy=proxy) as retry_response:
                        if retry_response.status == 200:
                            data = await retry_response.json()
                            print(f"Successfully retried page {page} for tag '{tag_label}' using proxy {proxy}")
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

async def search_plugins_by_tag(session: aiohttp.ClientSession, tag_label: str, tag_slug: str, sem: Semaphore) -> List[Dict]:
    """Search for plugins using the WordPress API by tag label asynchronously."""
    if is_tag_processed(tag_slug):
        print(f"Tag '{tag_label}' already processed for today, skipping.")
        return []
    
    params = {
        "action": "query_plugins",
        "search": tag_label,
        "page": 1,
        "per_page": 200
    }
    
    try:
        async with sem:
            # Get a working proxy
            proxy = await get_working_proxy()
            print(f"Using proxy {proxy} for initial request of tag '{tag_label}'")
            
            # Set a timeout of 10 seconds for the request
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with session.get(PLUGIN_API_BASE_URL, params=params, proxy=proxy, timeout=timeout) as response:
                if response.status != 200:
                    print(f"Failed to fetch initial data for tag '{tag_label}' using proxy {proxy}")
                    return []
                
                data = await response.json()
                total_pages = data.get('info', {}).get('pages', 1)
                all_plugins = data.get('plugins', [])  # First page plugins
                
                # Add a small delay after fetching the initial data
                await asyncio.sleep(0.5)  # Adjust the delay as needed
                
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

async def process_single_tag(session: aiohttp.ClientSession, tag: Dict, request_sem: Semaphore, tag_sem: Semaphore, tag_index: int, total_tags: int):
    """Process a single tag."""
    async with tag_sem:  # Limit concurrent tag processing
        tag_label_to_search = tag['label']
        tag_slug = tag['slug']
        
        start_time = time.time()
        print(f"\nStarting tag {tag_index + 1}/{total_tags}: {tag_label_to_search}")
        
        plugins = await search_plugins_by_tag(session, tag_label_to_search, tag_slug, request_sem)
        
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
    total_tags = len(tags)
    print(f"Starting processing of {total_tags} tags at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    request_sem = Semaphore(7)
    tag_sem = Semaphore(5)
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            process_single_tag(session, tag, request_sem, tag_sem, index, total_tags)
            for index, tag in enumerate(tags)
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

    
    test_tags = tags[:2000]
    
    # Run the async process
    asyncio.run(process_tags(test_tags)) 