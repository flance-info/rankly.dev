#!/usr/bin/env python3
import psycopg2
import logging
from multiprocessing import Pool, cpu_count
from datetime import datetime
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    filename='plugin_processor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database configuration
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

def process_single_plugin(plugin_data):
    """Process a single plugin"""
    plugin_id, plugin_slug, name, plugin_data = plugin_data
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        # Get tags and handle both list and dict formats
        tags = plugin_data.get('tags', [])
        if isinstance(tags, dict):
            tag_items = tags.items()
        else:
            tag_items = [(tag, tag) for tag in tags]
        
        # Process tags
        for tag_slug, tag_name in tag_items:
            # Insert or update tag
            cur.execute("""
                INSERT INTO tags (slug, name, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
                ON CONFLICT (slug) DO UPDATE 
                SET name = EXCLUDED.name,
                    updated_at = NOW()
            """, (tag_slug, tag_name))
            
            # Link tag to plugin
            cur.execute("""
                INSERT INTO plugin_tags (plugin_slug, tag_slug, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
                ON CONFLICT (plugin_slug, tag_slug) DO NOTHING
            """, (plugin_slug, tag_slug))
            
            # Insert keyword
            cur.execute("""
                INSERT INTO keywords (slug, name, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
                ON CONFLICT (slug) DO UPDATE 
                SET name = EXCLUDED.name,
                    updated_at = NOW()
            """, (tag_slug, tag_name))
        
        conn.commit()
        return True, name
        
    except Exception as e:
        conn.rollback()
        logging.error(f"Error processing plugin {name}: {str(e)}")
        return False, name
    finally:
        cur.close()
        conn.close()

def process_plugins():
    """Main function to process plugins in parallel"""
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        # Get all plugins
        cur.execute("""
            SELECT id, slug, name, plugin_data 
            FROM plugins
        """)
        plugins = cur.fetchall()
        total_plugins = len(plugins)
        
        # Determine number of processes
        num_processes = min(cpu_count(), 4)
        
        # Create process pool and process plugins in parallel with progress bar
        with Pool(num_processes) as pool:
            results = list(tqdm(
                pool.imap(process_single_plugin, plugins),
                total=total_plugins,
                desc="Processing plugins",
                unit="plugin"
            ))
        
        # Count successes and failures
        successes = sum(1 for success, _ in results if success)
        failures = sum(1 for success, _ in results if not success)
        
        print(f"\nResults:")
        print(f"✓ Successfully processed: {successes}")
        print(f"✗ Failed to process: {failures}")
        
        if failures > 0:
            print("\nFailed plugins:")
            for success, name in results:
                if not success:
                    print(f"- {name}")
        
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        raise
    finally:
        cur.close()
        conn.close()

def main():
    """Main entry point"""
    try:
        logging.info("Starting plugin processing job")
        process_plugins()
        logging.info("Finished plugin processing job")
    except Exception as e:
        logging.error(f"Job failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
