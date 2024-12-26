import psycopg2
import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters from environment variables
DB_CONNECTION = {
    'dbname': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# WordPress Plugin API Base URL
PLUGIN_API_BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"

def get_plugin_info(slug):
    """Fetch detailed plugin information from WordPress API."""
    params = {
        'action': 'plugin_information',
        'request[slug]': slug
    }
    
    try:
        response = requests.get(PLUGIN_API_BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch plugin info for {slug}: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching plugin info for {slug}: {e}")
        return None

def insert_plugin(conn, plugin_data):
    """Insert plugin data into the database."""
    cursor = conn.cursor()
    
    try:
        # Prepare the insert statement
        sql = """
        INSERT INTO plugins (
            name, 
            slug, 
            plugin_data,
            created_at,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (slug) 
        DO UPDATE SET 
            name = EXCLUDED.name,
            plugin_data = EXCLUDED.plugin_data,
            updated_at = EXCLUDED.updated_at
        """
        
        # Current timestamp for created_at and updated_at
        now = datetime.now()
        
        # Execute the insert
        cursor.execute(sql, (
            plugin_data.get('name', ''),
            plugin_data.get('slug', ''),
            json.dumps(plugin_data),
            now,
            now
        ))
        
        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted/updated plugin: {plugin_data.get('slug')}")
        
    except Exception as e:
        print(f"Error inserting plugin {plugin_data.get('slug')}: {e}")
        conn.rollback()
    finally:
        cursor.close()

def main():
    # List of plugin slugs to fetch
    plugin_slugs = [
        'woocommerce',
        'wordpress-seo',  # Yoast SEO
        'elementor',
        'wordfence',
        'contact-form-7',
        'string-locator'
        # Add more plugin slugs as needed
    ]
    
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONNECTION)
        print("Connected to database successfully")
        
        # Process each plugin
        for slug in plugin_slugs:
            print(f"\nProcessing plugin: {slug}")
            plugin_data = get_plugin_info(slug)
            
            if plugin_data:
                insert_plugin(conn, plugin_data)
            else:
                print(f"Skipping {slug} due to missing data")
                
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed")

if __name__ == "__main__":
    main() 