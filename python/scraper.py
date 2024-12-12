import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
import os

# Base URL for plugins
BASE_URL = "https://wp-rankings.com/plugins/page/{}/"

def fetch_page(page):
    """Fetch and process a single page."""
    print(f"Scraping page {page}...")
    response = requests.get(BASE_URL.format(page))
    if response.status_code != 200:
        print(f"Failed to fetch page {page}: {response.status_code}")
        return None  # Indicate failure

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all rows in the table
    rows = soup.find_all('tr', class_='geodir-post')
    if not rows:
        print(f"No rows found on page {page}. Exiting.")
        return "END"  # Indicate end of pages

    # Extract data from rows
    plugins = []
    for row in rows:
        try:
            # Extract rank
            rank_element = row.find('th', class_='fw-normal')
            rank = rank_element.text.strip() if rank_element else "N/A"
          
            # Extract plugin name and link
            plugin_cell = row.find('a', class_='stretched-linkx')
            if plugin_cell:
                plugin_name = plugin_cell.text.strip()
                plugin_link = plugin_cell.get('href', 'N/A')
            else:
                plugin_name = "N/A"
                plugin_link = "N/A"
            
            # Extract active installs
            active_installs_element = row.find_all('th', class_='fw-normal')[-1]
            active_installs = active_installs_element.text.strip() if active_installs_element else "N/A"
            
            # Extract positions
            position_cell = row.find('th', class_='fw-normal pt-2 pb-0')
            if position_cell:
                positions_div = position_cell.find('div', class_='fw-normal small text-muted')
                positions = positions_div.text.strip() if positions_div else "N/A"
            else:
                positions = "N/A"

            plugins.append({
                "Rank": rank,
                "Name": plugin_name,
                "Link": plugin_link,
                "Active Installs": active_installs,
                "Positions": positions
            })
        except Exception as e:
            print(f"Error parsing row on page {page}: {e}")
            continue

    return plugins

def save_plugins_to_file(plugins, filename="plugins_all_pages.json"):
    """Save plugins to a JSON file immediately."""
    if os.path.exists(filename):
        # Append to existing file
        with open(filename, "r+", encoding="utf-8") as file:
            existing_data = json.load(file)
            existing_data.extend(plugins)
            file.seek(0)
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
    else:
        # Create new file
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(plugins, file, ensure_ascii=False, indent=4)

def scrape_plugins():
    """Scrape plugin data with parallel requests."""
    filename = "plugins_all_pages.json"
    last_page = 1

    # Resume from last page if file exists
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            last_page = (len(data) // 20) + 1  # Assuming 20 plugins per page

    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=3) as executor:
        page = last_page
        while True:
            futures = {executor.submit(fetch_page, page + i): page + i for i in range(3)}
            for future in futures:
                page_number = futures[future]
                try:
                    result = future.result()
                    if result == "END":  # Stop if we reach the last page
                        print("All pages processed.")
                        return
                    elif result:  # Save data if the page is valid
                        save_plugins_to_file(result)
                except Exception as e:
                    print(f"Error processing page {page_number}: {e}")
            page += 3  # Move to the next batch of pages

if __name__ == "__main__":
    scrape_plugins()
