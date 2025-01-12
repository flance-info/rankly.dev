import os
import json
import logging
from datetime import datetime
import psycopg2
import time
from datetime import timedelta
import itertools
import random
import logging

# Configure logging
base_dir = os.path.dirname(__file__)
logs_dir = os.path.join(base_dir, 'logs')

# Ensure the logs directory exists
os.makedirs(logs_dir, exist_ok=True)
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_name = f'plugin_keyword_stats_{current_time}.log'
log_file_path = os.path.join(logs_dir, log_file_name)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def connect_db():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(
            dbname='laravel',
            user='laravel',
            password='secret',
            host='db',
            port='5432'
        )
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise

def load_json_data(file_path):
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading JSON file {file_path}: {e}")
        return None

def extract_date_from_filename(file_name):
    """Extract date from the file name."""
    try:
        # Assuming the format is 'xxx_plugins_YYYY-MM-DD.json'
        date_str = file_name.split('_')[-1].replace('.json', '')
        # Validate and return the date
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError as e:
        logging.error(f"Error parsing date from file name {file_name}: {e}")
        return None

def populate_plugin_keyword_stats_from_json(conn, json_data, stat_date):
    """Populate the plugin_keyword_stats table from JSON data."""
    tag_slug = json_data.get('tag_slug')
    plugins = json_data.get('plugins', [])

    for plugin in plugins:
        try:
            insert_plugin_keyword_stats(
                conn,
                plugin_slug=plugin['slug'],
                keyword_slug=tag_slug,
                stat_date=stat_date,
                rank_order=plugin['order'],
                active_installs=plugin.get('active_installs', 0),
                rating=plugin.get('rating', 0),
                num_ratings=plugin.get('num_ratings', 0),
                downloaded=plugin.get('downloaded', 0)
            )
            logging.info(f"Inserting plugin: {plugin['slug']}, keyword: {tag_slug}, date: {stat_date}, rank: {plugin['order']}, installs: {plugin.get('active_installs', 0)}, rating: {plugin.get('rating', 0)}, num_ratings: {plugin.get('num_ratings', 0)}, downloaded: {plugin.get('downloaded', 0)}")
        except Exception as e:
            logging.error(f"Error processing plugin {plugin['slug']}: {e}")

def main():
    # Establish a database connection
    conn = connect_db()

    # Use a relative path based on the script's directory
    base_dir = os.path.dirname(__file__)
    json_dir = os.path.join(base_dir, 'output', 'keywords')

    try:
        # Check if the directory exists
        if not os.path.exists(json_dir):
            logging.error(f"Directory does not exist: {json_dir}")
            return

        # Iterate over all JSON files in the directory
        for root, dirs, files in os.walk(json_dir):
            for file_name in files:
                logging.info(f"Processing file: {file_name}")
                if file_name.endswith('.json'):
                    file_path = os.path.join(root, file_name)
                    json_data = load_json_data(file_path)
                    stat_date = extract_date_from_filename(file_name)
                    if json_data and stat_date:
                        populate_plugin_keyword_stats_from_json(conn, json_data, stat_date)
    finally:
        # Close the database connection
        conn.close()


def insert_plugin_keyword_stats(conn, plugin_slug, keyword_slug, stat_date, rank_order, active_installs=0, rating=0, num_ratings=0, downloaded=0):
    """Insert plugin keyword stats into the database."""
    cursor = conn.cursor()
    
    try:
        # Check if the record already exists
        check_sql = """
        SELECT 1 FROM plugin_keyword_stats
        WHERE plugin_slug = %s AND keyword_slug = %s AND stat_date = %s
        """
        cursor.execute(check_sql, (plugin_slug, keyword_slug, stat_date))
        exists = cursor.fetchone()

        if exists:
            print(f"Record for plugin '{plugin_slug}' on date '{stat_date}' already exists. Skipping insertion.")
            return

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
        logging.info(f"Successfully inserted/updated keyword stats for plugin: {plugin_slug}")
        
    except Exception as e:
        # Debugging: Log the error and the values that caused it
        logging.error(f"Error inserting keyword stats for plugin {plugin_slug}: {e}")
        logging.error(f"Problematic values - plugin: {plugin_slug}, keyword: {keyword_slug}, date: {stat_date}, rank: {rank_order}, installs: {active_installs}, rating: {rating}, num_ratings: {num_ratings}, downloaded: {downloaded}")
        conn.rollback()
    finally:
        cursor.close()
             

if __name__ == "__main__":
    main() 