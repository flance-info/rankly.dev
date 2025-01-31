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
import logging
import psycopg2

# Configure logging
log_file_path = '/usr/src/app/logs/extract_search_key.log'
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Base directory for the output files
base_dir = os.path.dirname(__file__)

# Path to the tags file
tags_file = os.path.join(base_dir, "output", "tags.json")

# WordPress Plugin API Base URL
PLUGIN_API_BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"

# Updated list of proxies
proxies = [
    "194.169.202.177:6582",
    "64.64.115.243:5878",
    "91.211.87.122:7112",
    "89.43.32.83:5911",
    "161.123.131.225:5830",
    "185.226.205.12:5544",
    "92.42.0.6:6496",
    "104.222.167.103:6505",
    "104.239.2.208:6511",
    "104.250.204.44:6135",
    "192.177.87.67:5913",
    "104.253.91.66:6499",
    "31.58.32.69:6648",
    "45.131.94.239:6226",
    "64.137.124.59:6271",
    "89.43.32.144:5972",
    "191.96.170.43:5731",
    "136.0.88.158:5216",
    "161.123.101.132:6758",
    "193.178.227.81:6112",
    "45.61.98.12:5696",
    "92.112.168.164:6248",
    "92.112.171.12:5980",
    "188.208.16.233:7004",
    "46.203.206.248:5693",
    "84.33.210.23:5957",
    "145.223.53.62:6596",
    "107.173.36.181:5636",
    "45.61.97.105:6631",
    "23.129.253.212:6830"
]


DB_CONFIG = {
    'dbname': 'laravel',
    'user': 'laravel',
    'password': 'secret',
    'host': 'db',
    'port': '5432'
}

def connect_db():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise
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

def load_tags_from_db(conn):
    """Load tags from the 'keywords' table in the database, sorted by id."""
    cursor = conn.cursor()
    try:
        # Query to select all tags from the 'keywords' table, sorted by id
        cursor.execute("SELECT slug, name FROM keywords ORDER BY id")
        tags = cursor.fetchall()

        # Convert the result to a list of dictionaries
        return [{'slug': tag[0], 'label': tag[1]} for tag in tags]
    except Exception as e:
        print(f"Error loading tags from database: {e}")
        return []
    finally:
        cursor.close()

async def check_proxy(proxy: str) -> bool:
    """Check if a proxy is working by making a request to IP-API."""
    test_url = "http://ip-api.com/json/?fields=61439"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(test_url, proxy=f"http://{proxy}", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                   # print(f"Proxy {proxy} is working. IP: {data.get('query')}, City: {data.get('city')}")
                    return True
                else:
                    print(f"Proxy {proxy} failed with status: {response.status}")
                    return False
    except aiohttp.ClientProxyConnectionError as e:
        print(f"Proxy connection error for {proxy}: {e}")
    except aiohttp.ClientHttpProxyError as e:
        print(f"HTTP proxy error for {proxy}: {e}")
    except asyncio.TimeoutError:
        print(f"Timeout error for line 136 {proxy}")
    except Exception as e:
        print(f"Error checking proxy {proxy}: {e}")
    return False

async def get_working_proxy() -> str:
    """Get a random working proxy from the list."""
    while True:
        proxy = random.choice(proxies)
       ## if await check_proxy(proxy):
       ##     return proxy
       ## else:
       ##     print(f"Proxy {proxy} is not working, trying another...")
        return proxy

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
        "per_page": 300
    }

    async with sem:  # Limit concurrent requests
        try:
            # Reduce delay between requests
            await asyncio.sleep(1)  # Try with 0.5 seconds delay

            # Get a working proxy
            proxy = await get_working_proxy()

            async with session.get(PLUGIN_API_BASE_URL, params=params, proxy=f"http://{proxy}", timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return page, data.get('plugins', [])
                elif response.status == 429:
                    print(f"Rate limit hit for page {page} tag '{tag_label}', retrying after delay...")
                    await asyncio.sleep(30)  # Wait a full minute before retry
                    # Retry the request
                    async with session.get(PLUGIN_API_BASE_URL, params=params, proxy=f"http://{proxy}", timeout=30) as retry_response:
                        if retry_response.status == 200:
                            data = await retry_response.json()
                            return page, data.get('plugins', [])
                        else:
                            print(f"Failed retry for page {page} tag '{tag_label}': {retry_response.status}")
                            return page, []
                else:
                    print(f"Failed to fetch page {page} for tag '{tag_label}': {response.status}")
                    return page, []
        except aiohttp.ClientProxyConnectionError as e:
            print(f"Proxy connection error for {proxy}: {e}")
        except aiohttp.ClientHttpProxyError as e:
            print(f"HTTP proxy error for {proxy}: {e}")
        except asyncio.TimeoutError:
            print(f"Timeout error for l-198 {proxy}")
        except Exception as e:
            print(f"Error fetching page {page} for tag '{tag_label}': {e}")
        return page, []

async def search_plugins_by_tag(session: aiohttp.ClientSession, tag_label: str, tag_slug: str, sem: Semaphore) -> List[Dict]:
    """Search for plugins using the WordPress API by tag label asynchronously."""
    # if is_tag_processed(tag_slug):
    #    print(f"Tag '{tag_label}' already processed for today, skipping.")
    #    return []

    params = {
        "action": "query_plugins",
        "search": tag_label,
        "page": 1,
        "per_page": 300
    }

    try:
        async with sem:
            # Get a working proxy
            proxy = await get_working_proxy()
            #print(f"Using proxy {proxy} for initial request of tag '{tag_label}'")

            # Set a timeout of 10 seconds for the request
            timeout = aiohttp.ClientTimeout(total=30)

            async with session.get(PLUGIN_API_BASE_URL, params=params, proxy=f"http://{proxy}", timeout=timeout) as response:
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

    except aiohttp.ClientProxyConnectionError as e:
        print(f"Proxy connection error for {proxy}: {e}")
    except aiohttp.ClientHttpProxyError as e:
        print(f"HTTP proxy error for {proxy}: {e}")
    except asyncio.TimeoutError:
        print(f"Timeout error for line 261 {proxy}")
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
        conn = connect_db()
        cur = conn.cursor()
        if plugins:
          #save_results_to_file(plugins, tag_slug, tag_label_to_search)
          process_and_store_plugins(conn, plugins, tag_slug)
        else:
            print(f"No plugins found for tag '{tag_label_to_search}'")

async def process_tags(tags: List[Dict]):
    """Process multiple tags concurrently."""

    start_time = time.time()
    total_tags = len(tags)
    print(f"Starting processing of {total_tags} tags at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    request_sem = Semaphore(40)
    tag_sem = Semaphore(30)

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

def insert_plugin_keyword_stats(conn, plugin_slug, keyword_slug, stat_date, rank_order, active_installs=0, rating=0, num_ratings=0, downloaded=0):
    """Insert plugin keyword stats into the database."""
    cursor = conn.cursor()

    try:
        # Start time measurement
        #start_time = time.time()

        # Check if the record already exists
        #check_sql = """
        #SELECT 1 FROM plugin_keyword_stats
        #WHERE plugin_slug = %s AND keyword_slug = %s AND stat_date = %s
        #"""
      #  cursor.execute(check_sql, (plugin_slug, keyword_slug, stat_date))
      #  exists = cursor.fetchone()

        # End time measurement
        #end_time = time.time()
        #query_duration = end_time - start_time

        # Log the time taken for the query
        #print(f"Query execution time: {query_duration:.4f} seconds for select")

        #if exists:
           # logging.info(f"Record for plugin '{plugin_slug}' on date '{stat_date}' already exists. Skipping insertion.")
        #    return
        #start_time = time.time()
        # Proceed with insertion if the record does not exist
        sql = """
        INSERT INTO plugin_keyword_stats (
            plugin_slug,
            keyword_slug,
            stat_date,
            rank_order,
            active_installs,
            rating,
            num_ratings,
            created_at,
            updated_at,
            downloaded
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (plugin_slug, keyword_slug, stat_date)
        DO UPDATE SET
            rank_order = EXCLUDED.rank_order,
            active_installs = COALESCE(EXCLUDED.active_installs, plugin_keyword_stats.active_installs),
            rating = COALESCE(EXCLUDED.rating, plugin_keyword_stats.rating),
            num_ratings = COALESCE(EXCLUDED.num_ratings, plugin_keyword_stats.num_ratings),
            downloaded = COALESCE(EXCLUDED.downloaded, plugin_keyword_stats.downloaded),
            updated_at = EXCLUDED.updated_at
        """

        now = datetime.now()

        # Debugging: Log the values being inserted
        #logging.info(f"Inserting plugin: {plugin_slug}, keyword: {keyword_slug}, date: {stat_date}, rank: {rank_order}, installs: {active_installs}, rating: {rating}, num_ratings: {num_ratings}, downloaded: {downloaded}")

        cursor.execute(sql, (
            plugin_slug,
            keyword_slug,
            stat_date,
            rank_order,
            active_installs,
            rating,
            num_ratings,
            now,
            now,
            downloaded
        ))

        conn.commit()
        #print(f"Inserting plugin: {plugin_slug}, keyword: {keyword_slug}, date: {stat_date}, rank: {rank_order}, installs: {active_installs}, rating: {rating}, num_ratings: {num_ratings}, downloaded: {downloaded}")

        #end_time = time.time()
        #query_duration = end_time - start_time
        #logging.info(f"Inserting plugin: {plugin_slug}, keyword: {keyword_slug}, date: {stat_date}, rank: {rank_order}, installs: {active_installs}, rating: {rating}, num_ratings: {num_ratings}, downloaded: {downloaded}")
          # Log the time taken for the query
        #print(f"Query execution time: {query_duration:.4f} seconds for insert")
    except Exception as e:
        # Debugging: Log the error and the values that caused it
       # logging.error(f"Error inserting keyword stats for plugin {plugin_slug}: {e}")
        logging.error(f"Problematic values - plugin: {plugin_slug}, keyword: {keyword_slug}, date: {stat_date}, rank: {rank_order}, installs: {active_installs}, rating: {rating}, num_ratings: {num_ratings}, downloaded: {downloaded}")
        conn.rollback()
    finally:
        cursor.close()

def process_and_store_plugins(conn, plugins, tag_slug):
    """Process and store plugin data into the database."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    for rank_order, plugin in enumerate(plugins, start=1):
        try:
            insert_plugin_keyword_stats(
                conn,
                plugin_slug=plugin['slug'],
                keyword_slug=tag_slug,
                stat_date=current_date,
                rank_order=rank_order,
                active_installs=plugin.get('active_installs', 0),
                rating=plugin.get('rating', 0),
                num_ratings=plugin.get('num_ratings', 0),
                downloaded=plugin.get('downloaded', 0)
            )
           # print(f"Successfully inserted/updated keyword stats for plugin: {plugin['slug']}")
        except Exception as e:
            print(f"Error inserting keyword stats for plugin {plugin['slug']}: {e}")

async def fetch_with_retry(session, url, proxy, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url, proxy=f"http://{proxy}", timeout=10) as response:
                return await response.json()
        except asyncio.TimeoutError:
            print(f"Timeout error for attempt {attempt + 1} with proxy {proxy}")
            if attempt < retries - 1:
                await asyncio.sleep(2)  # Wait before retrying
            else:
                print(f"Failed to fetch data after {retries} attempts")
                return None

def main():
    # Establish a database connection
    conn = connect_db()

    # tags = load_tags(tags_file)


    # test_tags = tags[:2000]

    # Run the async process
    # asyncio.run(process_tags(test_tags))

    try:
        # Load tags from the database
        tags = load_tags_from_db(conn)
        test_tags = tags[:60000];

        # Process the tags
        asyncio.run(process_tags(test_tags))
    finally:
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    main()
