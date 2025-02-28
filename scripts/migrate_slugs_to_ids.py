import psycopg2
from psycopg2.extras import DictCursor

def migrate_slugs_to_ids():
    conn = None
    try:
        # Connect to your database
        conn = psycopg2.connect(
            dbname="rankly",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor(cursor_factory=DictCursor)

        # Step 1: Get all plugin_keyword_stats records
        cur.execute("SELECT * FROM plugin_keyword_stats")
        stats = cur.fetchall()

        # Step 2: Create temporary columns
        cur.execute("""
            ALTER TABLE plugin_keyword_stats
            ADD COLUMN IF NOT EXISTS temp_plugin_id BIGINT,
            ADD COLUMN IF NOT EXISTS temp_keyword_id BIGINT
        """)

        # Step 3: Update records with proper IDs
        updated = 0
        for stat in stats:
            # Get plugin ID
            cur.execute(
                "SELECT id FROM plugins WHERE slug = %s",
                (stat['plugin_slug'],)
            )
            plugin = cur.fetchone()
            if not plugin:
                print(f"Plugin not found for slug: {stat['plugin_slug']}")
                continue

            # Get keyword ID
            cur.execute(
                "SELECT id FROM keywords WHERE slug = %s",
                (stat['keyword_slug'],)
            )
            keyword = cur.fetchone()
            if not keyword:
                print(f"Keyword not found for slug: {stat['keyword_slug']}")
                continue

            # Update the record
            cur.execute("""
                UPDATE plugin_keyword_stats
                SET 
                    temp_plugin_id = %s,
                    temp_keyword_id = %s
                WHERE plugin_slug = %s 
                    AND keyword_slug = %s 
                    AND stat_date = %s
            """, (
                plugin['id'],
                keyword['id'],
                stat['plugin_slug'],
                stat['keyword_slug'],
                stat['stat_date']
            ))
            updated += 1

        # Step 4: Finalize the migration
        cur.execute("""
            ALTER TABLE plugin_keyword_stats
            DROP COLUMN plugin_slug,
            DROP COLUMN keyword_slug,
            RENAME COLUMN temp_plugin_id TO plugin_id,
            RENAME COLUMN temp_keyword_id TO keyword_id
        """)

        conn.commit()
        print(f"Successfully migrated {updated} records")

    except Exception as e:
        print(f"Error: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_slugs_to_ids() 