#!/usr/bin/env python3
import psycopg2
import logging
from tqdm import tqdm

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

def process_plugins_simple():
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id, slug, name, plugin_data FROM plugins")
        plugins = cur.fetchall()
        
        # Main progress bar for plugins
        with tqdm(plugins, desc="Processing plugins") as pbar:
            for plugin in pbar:
                plugin_id, plugin_slug, name, plugin_data = plugin
                pbar.set_description(f"Plugin: {name[:30]}...")
                
                # Debug: Check plugin details
                print(f"\nProcessing plugin:")
                print(f"ID: {plugin_id}")
                print(f"Slug length: {len(plugin_slug)} - {plugin_slug}")
                print(f"Name length: {len(name)} - {name}")
                
                tags = plugin_data.get('tags', [])
                if isinstance(tags, dict):
                    tag_items = tags.items()
                else:
                    tag_items = [(tag, tag) for tag in tags]
                
                # Debug: Check tag details
                print("\nTags to process:")
                for tag_slug, tag_name in tag_items:
                    print(f"Tag slug length: {len(tag_slug)} - {tag_slug}")
                    print(f"Tag name length: {len(tag_name)} - {tag_name}")
                
                # Nested progress bar for tags
                for tag_slug, tag_name in tqdm(tag_items, 
                                             desc="Tags", 
                                             leave=False, 
                                             position=1):
                    try:
                        # Debug: Print values before insert
                        print(f"\nAttempting to insert:")
                        print(f"Tag slug ({len(tag_slug)}): {tag_slug}")
                        print(f"Tag name ({len(tag_name)}): {tag_name}")
                        
                        # Direct inserts without any text processing
                        cur.execute("""
                            INSERT INTO tags (slug, name, created_at, updated_at)
                            VALUES (%s, %s, NOW(), NOW())
                            ON CONFLICT (slug) DO UPDATE 
                            SET name = EXCLUDED.name
                        """, (tag_slug, tag_name))
                        
                        cur.execute("""
                            INSERT INTO plugin_tags (plugin_slug, tag_slug, created_at, updated_at)
                            VALUES (%s, %s, NOW(), NOW())
                            ON CONFLICT (plugin_slug, tag_slug) DO NOTHING
                        """, (plugin_slug, tag_slug))
                        
                        cur.execute("""
                            INSERT INTO keywords (slug, name, created_at, updated_at)
                            VALUES (%s, %s, NOW(), NOW())
                            ON CONFLICT (slug) DO NOTHING
                        """, (tag_slug, tag_name))
                        
                    except Exception as e:
                        print(f"\nError on specific insert:")
                        print(f"Plugin: {name}")
                        print(f"Tag slug: {tag_slug}")
                        print(f"Tag name: {tag_name}")
                        print(f"Error: {str(e)}")
                        raise
                
                conn.commit()
            
    except Exception as e:
        conn.rollback()
        print(f"\nFinal error: {str(e)}")
        raise
    finally:
        cur.close()
        conn.close()

def main():
    """Main entry point"""
    try:
        print("Starting plugin processing job")
        process_plugins_simple()
        print("\nFinished plugin processing job")
    except Exception as e:
        print(f"\nJob failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 