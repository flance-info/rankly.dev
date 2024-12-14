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
    "http://45.202.78.210:3128",
    "http://156.253.165.189:3128",
    "http://45.202.77.34:3128",
    "http://156.228.88.150:3128",
    "http://156.228.178.250:3128",
    "http://104.167.27.97:3128",
    "http://154.213.193.104:3128",
    "http://104.167.31.56:3128",
    "http://156.228.103.215:3128",
    "http://156.253.178.52:3128",
    "http://156.228.113.202:3128",
    "http://156.249.138.86:3128",
    "http://156.233.94.219:3128",
    "http://154.213.196.245:3128",
    "http://156.233.73.53:3128",
    "http://104.167.28.83:3128",
    "http://104.207.62.234:3128",
    "http://156.228.105.201:3128",
    "http://156.228.88.66:3128",
    "http://156.228.178.162:3128",
    "http://104.207.47.39:3128",
    "http://156.228.101.242:3128",
    "http://156.228.91.177:3128",
    "http://104.207.34.34:3128",
    "http://156.228.77.207:3128",
    "http://154.213.197.123:3128",
    "http://104.207.58.66:3128",
    "http://104.167.31.182:3128",
    "http://104.207.34.181:3128",
    "http://154.94.15.236:3128",
    "http://156.228.184.223:3128",
    "http://45.201.11.43:3128",
    "http://156.228.189.182:3128",
    "http://156.253.164.175:3128",
    "http://154.213.197.9:3128",
    "http://156.253.179.132:3128",
    "http://154.213.198.196:3128",
    "http://156.228.125.69:3128",
    "http://156.253.173.50:3128",
    "http://156.228.77.94:3128",
    "http://104.207.37.101:3128",
    "http://156.228.171.227:3128",
    "http://104.207.47.64:3128",
    "http://154.213.197.27:3128",
    "http://156.228.100.247:3128",
    "http://154.213.204.13:3128",
    "http://104.207.51.108:3128",
    "http://156.253.166.127:3128",
    "http://156.228.89.186:3128",
    "http://156.249.138.17:3128",
    "http://156.228.93.242:3128",
    "http://104.167.27.35:3128",
    "http://45.202.77.40:3128",
    "http://156.233.75.38:3128",
    "http://156.228.97.247:3128",
    "http://154.213.193.231:3128",
    "http://104.207.37.9:3128",
    "http://156.233.85.173:3128",
    "http://156.228.90.47:3128",
    "http://104.207.55.102:3128",
    "http://156.233.85.118:3128",
    "http://104.207.36.164:3128",
    "http://156.253.177.153:3128",
    "http://156.228.88.216:3128",
    "http://156.233.72.3:3128",
    "http://156.253.164.182:3128",
    "http://104.207.44.31:3128",
    "http://156.228.180.14:3128",
    "http://156.228.102.122:3128",
    "http://104.207.60.59:3128",
    "http://156.228.81.69:3128",
    "http://154.213.202.61:3128",
    "http://104.207.46.62:3128",
    "http://104.167.28.112:3128",
    "http://104.207.50.124:3128",
    "http://156.233.89.233:3128",
    "http://156.228.110.36:3128",
    "http://156.228.79.214:3128",
    "http://156.228.105.161:3128",
    "http://154.213.202.79:3128",
    "http://156.240.99.24:3128",
    "http://156.228.108.183:3128",
    "http://156.228.182.236:3128",
    "http://154.94.13.90:3128",
    "http://156.228.117.205:3128",
    "http://104.207.41.139:3128",
    "http://154.213.202.32:3128",
    "http://156.233.88.206:3128",
    "http://156.228.108.104:3128",
    "http://104.207.62.118:3128",
    "http://104.167.31.172:3128",
    "http://156.228.174.162:3128",
    "http://104.167.29.204:3128",
    "http://154.213.203.88:3128",
    "http://156.228.90.35:3128",
    "http://156.228.80.37:3128",
    "http://156.228.190.248:3128",
    "http://156.228.185.132:3128",
    "http://104.207.32.116:3128",
    "http://156.228.110.124:3128"
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
                    print(f"Proxy {proxy} is working. IP: {data.get('query')}")
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
                    await asyncio.sleep(60)  # Wait a full minute before retry
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
            # Get a working proxy
            proxy = await get_working_proxy()
            print(f"Using proxy {proxy} for initial request of tag '{tag_label}'")
            
            async with session.get(PLUGIN_API_BASE_URL, params=params, proxy=proxy) as response:
                if response.status != 200:
                    print(f"Failed to fetch initial data for tag '{tag_label}' using proxy {proxy}")
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
    
    request_sem = Semaphore(15)
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