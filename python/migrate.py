import psycopg2
import logging

# Database configuration
DB_HOST = "laravel-db"
DB_PORT = "5432"
DB_NAME = "laravel-live-backup"
DB_USER = "laravel"
DB_PASS = "secret"

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def table_exists(conn, table_name, schema='public'):
    """Check if a table exists in the database."""
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = %s
                  AND table_name = %s
            );
        """, (schema, table_name))
        return cur.fetchone()[0]
    finally:
        cur.close()

def create_migration_progress_table(conn):
    """Create the migration_progress table if it doesn't exist."""
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS migration_progress (
                step TEXT PRIMARY KEY,
                status TEXT,
                started_at TIMESTAMP DEFAULT NOW(),
                completed_at TIMESTAMP
            );
        """)
        conn.commit()
        logging.info("Created 'migration_progress' table.")
    finally:
        cur.close()

def insert_migration_progress(conn, step, status):
    """Insert or update migration progress in the database."""
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO migration_progress (step, status) 
            VALUES (%s, %s)
            ON CONFLICT (step) DO UPDATE SET status = EXCLUDED.status;
        """, (step, status))
        conn.commit()
        logging.info(f"Updated migration progress: step={step}, status={status}")
    finally:
        cur.close()

def add_new_columns(conn):
    """Add new columns to the plugin_keyword_stats table if they don't exist."""
    cur = conn.cursor()
    try:
        # Check if the columns already exist
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'plugin_keyword_stats'
              AND (column_name = 'plugin_id' OR column_name = 'keyword_id');
        """)
        existing_columns = [row[0] for row in cur.fetchall()]

        # Add columns only if they don't exist
        if 'plugin_id' not in existing_columns:
            cur.execute("ALTER TABLE plugin_keyword_stats ADD COLUMN plugin_id bigint;")
            logging.info("Added 'plugin_id' column to plugin_keyword_stats table.")
        else:
            logging.info("'plugin_id' column already exists in plugin_keyword_stats table.")

        if 'keyword_id' not in existing_columns:
            cur.execute("ALTER TABLE plugin_keyword_stats ADD COLUMN keyword_id bigint;")
            logging.info("Added 'keyword_id' column to plugin_keyword_stats table.")
        else:
            logging.info("'keyword_id' column already exists in plugin_keyword_stats table.")

        conn.commit()
    finally:
        cur.close()

def count_rows_in_batches(conn, table_name, batch_size=50):
    """Count rows in batches and display progress."""
    logging.info("info: Counting rows in batches.")
    cur = conn.cursor()
    try:
        total_rows = 0
        processed_rows = 0
        logging.info(f"Counting rows in {table_name} table.")
      
        logging.info(f"Batch size: {batch_size}")
        while True:
            cur.execute("""
                SELECT COUNT(*) 
                FROM {} 
                WHERE id > %s 
                LIMIT %s;
            """.format(table_name), (processed_rows, batch_size))
            batch_count = cur.fetchone()[0]
            logging.info(f"Counted {batch_count} rows.")
            if batch_count == 0:
                break

            total_rows += batch_count
            processed_rows += batch_count

            progress = (processed_rows / (total_rows + processed_rows)) * 100 if total_rows > 0 else 0
            logging.info(f"Counted {processed_rows} rows ({progress:.2f}%)")

        logging.info(f"Total rows counted: {total_rows}")
        return total_rows
    finally:
        cur.close()


def create_temporary_indexes(conn, batch_size=50):
    """Create temporary indexes for optimization in smaller batches and display progress."""
    cur = conn.cursor()
    try:
        # Use the new method to count rows
       # total_rows = count_rows_in_batches(conn, 'plugin_keyword_stats', batch_size)
        total_rows = 115308339;
        # Create index on plugin_slug in batches
        logging.info("info: selecting total rows.")
       
        processed_rows = 0
        logging.info(f"Total rows to process: {total_rows}")
        while processed_rows < total_rows:
            # Turn off autocommit for this specific operation
            conn.autocommit = True
            cur.execute("""
                CREATE INDEX CONCURRENTLY IF NOT EXISTS tmp_plugin_slug_idx_batch_{} 
                ON plugin_keyword_stats (plugin_slug) 
                WHERE id BETWEEN %s AND %s;
            """.format(processed_rows // batch_size), (processed_rows + 1, min(processed_rows + batch_size, total_rows)))
            conn.autocommit = False  # Turn autocommit back off

            processed_rows += batch_size
            progress = (processed_rows / total_rows) * 100
            logging.info(f"Created batch of 'tmp_plugin_slug_idx' index: Processed {processed_rows}/{total_rows} rows ({progress:.2f}%)")

        # Combine the batch indexes into a single index
        conn.autocommit = True
        cur.execute("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS tmp_plugin_slug_idx 
            ON plugin_keyword_stats (plugin_slug);
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_0;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_1;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_2;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_3;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_4;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_5;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_6;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_7;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_8;
            DROP INDEX IF EXISTS tmp_plugin_slug_idx_batch_9;
        """)
        conn.autocommit = False
        logging.info("Combined 'tmp_plugin_slug_idx' index.")

        # Create index on keyword_slug in batches
        processed_rows = 0
        while processed_rows < total_rows:
            conn.autocommit = True
            cur.execute("""
                CREATE INDEX CONCURRENTLY IF NOT EXISTS tmp_keyword_slug_idx_batch_{} 
                ON plugin_keyword_stats (keyword_slug) 
                WHERE id BETWEEN %s AND %s;
            """.format(processed_rows // batch_size), (processed_rows + 1, min(processed_rows + batch_size, total_rows)))
            conn.autocommit = False

            processed_rows += batch_size
            progress = (processed_rows / total_rows) * 100
            logging.info(f"Created batch of 'tmp_keyword_slug_idx' index: Processed {processed_rows}/{total_rows} rows ({progress:.2f}%)")

        # Combine the batch indexes into a single index
        conn.autocommit = True
        cur.execute("""
            CREATE INDEX CONCURRENTLY IF NOT EXISTS tmp_keyword_slug_idx 
            ON plugin_keyword_stats (keyword_slug);
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_0;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_1;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_2;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_3;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_4;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_5;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_6;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_7;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_8;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx_batch_9;
        """)
        conn.autocommit = False
        logging.info("Combined 'tmp_keyword_slug_idx' index.")

    finally:
        cur.close()

def update_migration_progress(conn, status):
    """Update the migration progress in the migration_progress table."""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE migration_progress 
            SET status = %s 
            WHERE step = 'schema_migration';
        """, (status,))
        conn.commit()
        logging.info(f"Updated migration progress to '{status}'.")
    finally:
        cur.close() 
def populate_new_columns(conn, batch_size=1000):
    """Populate new columns with IDs for valid slugs in batches, showing progress."""
    cur = conn.cursor()
    try:
        # Start transaction
        conn.autocommit = False

        # Prepare the UPDATE statement
        update_sql = """
            UPDATE plugin_keyword_stats pks
            SET 
                plugin_id = %s,
                keyword_id = %s
            WHERE pks.id = %s;
        """
# add here logging
        logging.info("Populating new columns with IDs.")
        # Count total rows to process
        #cur.execute("""
        #    SELECT COUNT(*) 
        #    FROM plugin_keyword_stats pks
        #    JOIN plugins p ON pks.plugin_slug = p.slug
        #    JOIN keywords k ON pks.keyword_slug = k.slug
        #    WHERE pks.plugin_slug IS NOT NULL
        #    AND pks.keyword_slug IS NOT NULL;
       # """)
        #total_rows = cur.fetchone()[0]
        total_rows = 115308339;
        logging.info(f"Total rows to process: {total_rows}")
        processed_rows = 0

        # Process data in batches
        while True:
            cur.execute("""
                SELECT pks.id, p.id AS plugin_id, k.id AS keyword_id
                FROM plugin_keyword_stats pks
                JOIN plugins p ON pks.plugin_slug = p.slug
                JOIN keywords k ON pks.keyword_slug = k.slug
                WHERE pks.plugin_slug IS NOT NULL
                  AND pks.keyword_slug IS NOT NULL
                OFFSET %s LIMIT %s;
            """, (processed_rows, batch_size))
            batch = cur.fetchall()

            if not batch:
                break

            # Execute the batch update
            cur.executemany(update_sql, [(row[1], row[2], row[0]) for row in batch])

            # Commit the batch
            conn.commit()

            # Update progress and log the updated row ID
            for row in batch:
                processed_rows += 1
                progress = (processed_rows / total_rows) * 100
                logging.info(f"Updated row ID: {row[0]}, Processed {processed_rows}/{total_rows} rows ({progress:.2f}%)")

            # Stop after processing one row
           # if processed_rows >= 1:                break

        logging.info("Populated new columns with IDs.")

    finally:
        cur.close()

def mark_migration_completion(conn):
    """Mark the migration as completed in the migration_progress table."""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE migration_progress 
            SET status = 'completed', completed_at = NOW() 
            WHERE step = 'schema_migration';
        """)
        conn.commit()
        logging.info("Marked migration as completed.")
    finally:
        cur.close()

def drop_old_constraints_and_add_new(conn):
    """Drop old constraints, add new ones, and drop old columns."""
    cur = conn.cursor()
    try:
        cur.execute("""
            ALTER TABLE plugin_keyword_stats
                DROP CONSTRAINT IF EXISTS plugin_keyword_stats_plugin_slug_foreign,
                DROP CONSTRAINT IF EXISTS plugin_keyword_stats_keyword_slug_foreign,
                ADD CONSTRAINT plugin_keyword_stats_plugin_id_foreign 
                    FOREIGN KEY (plugin_id) REFERENCES plugins(id) ON DELETE CASCADE,
                ADD CONSTRAINT plugin_keyword_stats_keyword_id_foreign 
                    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
                DROP COLUMN IF EXISTS plugin_slug,
                DROP COLUMN IF EXISTS keyword_slug;
        """)
        conn.commit()
        logging.info("Dropped old constraints, added new ones, and dropped old columns.")
    finally:
        cur.close()       

def drop_temporary_indexes(conn):
    """Drop temporary indexes."""
    cur = conn.cursor()
    try:
        cur.execute("""
            DROP INDEX IF EXISTS tmp_plugin_slug_idx;
            DROP INDEX IF EXISTS tmp_keyword_slug_idx;
        """)
        conn.commit()
        logging.info("Dropped temporary indexes.")
    finally:
        cur.close()


def run_migration(conn):
    """Run the SQL migration."""
    cur = conn.cursor()
    try:
        conn.autocommit = False
        # Check if the migration_progress table exists
        if not table_exists(conn, 'migration_progress'):
            create_migration_progress_table(conn)
            
        if table_exists(conn, 'migration_progress'):
            logging.info("'migration_progress' table exists.")
        else:
            logging.error("'migration_progress' table does not exist.")

        insert_migration_progress(conn, 'schema_migration', 'started');
        add_new_columns(conn)
        logging.info("Added new columns.")
        drop_temporary_indexes(conn)
        logging.info("info: Dropped temporary indexes.")
        logging.info("info: Creating temporary indexes.")
        # Create temporary indexes
        # create_temporary_indexes(conn)
        logging.info("info: Created temporary indexes.")
        # Update progress to 'adding_columns'
        update_migration_progress(conn, 'adding_columns')
        logging.info("Updated progress to 'adding_columns'.")
        # Populate new columns
        populate_new_columns(conn)
        logging.info("Populated new columns.")

        # Mark migration as completed
        mark_migration_completion(conn)
        logging.info("Marked migration as completed.")
        # Drop old constraints, add new ones, and drop old columns
       # drop_old_constraints_and_add_new(conn)

        # Drop temporary indexes
        drop_temporary_indexes(conn)
        logging.info("Dropped temporary indexes.")
        conn.commit()
        logging.info("Migration completed successfully.")
    except Exception as e:
        logging.error(f"Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()

def verify_migration(conn):
    """Verify the migration results."""
    cur = conn.cursor()
    try:
        # Verify foreign key constraints
        cur.execute("""
        SELECT 
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
            ON tc.constraint_name = ccu.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_name = 'plugin_keyword_stats';
        """)
        results = cur.fetchall()
        logging.info("Foreign key verification results:")
        for row in results:
            logging.info(row)
    except Exception as e:
        logging.error(f"Error verifying migration: {e}")
        raise
    finally:
        cur.close()

def main():
    """Main function to run the migration."""
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        logging.info("Connected to the database.")

        # Run the migration
        run_migration(conn)

        # Verify the migration results
        verify_migration(conn)

    except Exception as e:
        logging.error(f"Migration failed: {e}")
    finally:
        if conn:
            conn.close()
        logging.info("Migration process completed.")

if __name__ == "__main__":
    main()
