import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
URL = "https://wp-rankings.com/plugins/"

def scrape_plugins():
    """Scrape the plugin data from the website."""
    # Fetch the webpage content
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Failed to fetch webpage: {response.status_code}")
        return
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all rows in the table
    rows = soup.find_all('tr', class_='geodir-post')
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
            print(f"Error parsing row: {e}")
            continue
    
    # Save results to JSON
    with open("plugins.json", "w", encoding="utf-8") as json_file:
        json.dump(plugins, json_file, ensure_ascii=False, indent=4)
    print(f"Results saved to plugins.json")

if __name__ == "__main__":
    scrape_plugins()
