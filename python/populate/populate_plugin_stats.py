import psycopg2
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_CONNECTION = {
    'dbname': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def insert_plugin_stats(conn, plugin_data):
    """Insert plugin statistics into the plugin_stats table."""
    cursor = conn.cursor()
    
    try:
        sql = """
        INSERT INTO plugin_stats (
            plugin_slug,
            stat_date,
            active_installs,
            downloaded,
            support_threads,
            support_threads_resolved,
            created_at,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (plugin_slug, stat_date) 
        DO UPDATE SET
            active_installs = EXCLUDED.active_installs,
            downloaded = EXCLUDED.downloaded,
            support_threads = EXCLUDED.support_threads,
            support_threads_resolved = EXCLUDED.support_threads_resolved,
            updated_at = EXCLUDED.updated_at
        """
        
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')  # Format date as YYYY-MM-DD
        
        cursor.execute(sql, (
            plugin_data.get('slug', ''),
            today,
            plugin_data.get('active_installs', 0),
            plugin_data.get('downloaded', 0),
            plugin_data.get('support_threads', 0),
            plugin_data.get('support_threads_resolved', 0),
            now,
            now
        ))
        
        conn.commit()
        print(f"Successfully inserted stats for plugin: {plugin_data.get('slug')} (Date: {today})")
        
    except Exception as e:
        print(f"Error inserting stats for plugin {plugin_data.get('slug')}: {e}")
        conn.rollback()
    finally:
        cursor.close()

