import os
import sqlite3 
import logging
import pandas as pd
from datetime import datetime, timezone
from config import DATABASE
from detected_object import DetectedObject
from logger import app_logger

class DB:
    def __init__(self, db_path=DATABASE):
        self.db_path = db_path
        self.table_name = "objects"
        
        # Check if the database file exists
        if not os.path.exists(self.db_path):
            app_logger.info(f"Database file {self.db_path} not found. Creating a new database.")
        try:
            # Try to create tables (if the database does not exist, this will initialize it)
            self._create_tables()
            app_logger.info(f"Database initialized, connected to {self.db_path}")
        except Exception as e:
            app_logger.error(f"Error initializing database: {str(e)}")

    def _connect(self):
        """Create a new SQLite connection."""
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            app_logger.error(f"Error connecting to the database: {str(e)}")
            raise

    def _create_tables(self):
        """Create tables if they don't exist using a new connection."""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        object_id INTEGER UNIQUE,
                        first_detected_time TEXT,
                        last_detected_time TEXT,
                        class_name TEXT,
                        class_id INTEGER
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS object_counts (
                        timestamp TEXT PRIMARY KEY,
                        count INTEGER NOT NULL
                    )
                ''')
                conn.commit()
                app_logger.info("Tables created or already exist in the database.")
        except Exception as e:
            app_logger.error(f"Error creating tables: {str(e)}")
            raise

    def add_object(self, detected_object: DetectedObject):
        """Add a new object to the database or update its last_detected_time."""
        if detected_object.object_id is None:
            app_logger.warning(f"Object ID is None, skipping add_object for {detected_object}")
            return
        
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                # Insert or ignore if object already exists
                cursor.execute(f'''
                    INSERT OR IGNORE INTO {self.table_name} (object_id, first_detected_time, last_detected_time, class_name, class_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (detected_object.object_id, detected_object.first_detected_time, detected_object.last_detected_time, detected_object.class_name, detected_object.class_id))
                
                # Update last_detected_time if the object already exists
                cursor.execute(f'''
                    UPDATE {self.table_name}
                    SET last_detected_time = ?
                    WHERE object_id = ?
                ''', (detected_object.last_detected_time, detected_object.object_id))
                
                conn.commit()
                app_logger.debug(f"Object {detected_object.object_id} added/updated in the database.")
        except Exception as e:
            app_logger.error(f"Error adding/updating object {detected_object.object_id}: {str(e)}")

    def update_object(self, detected_object: DetectedObject):
        """Update the last_detected_time of an object."""
        if detected_object.object_id is None:
            app_logger.warning(f"Object ID is None, skipping update_object for {detected_object}")
            return
        
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    UPDATE {self.table_name}
                    SET last_detected_time = ?
                    WHERE object_id = ?
                ''', (detected_object.last_detected_time, detected_object.object_id))
                conn.commit()
                app_logger.info(f"Object {detected_object.object_id} updated in the database.")
        except Exception as e:
            app_logger.error(f"Error updating object {detected_object.object_id}: {str(e)}")

    def get_total_objects(self, object_class):
        """Get the total number of unique objects detected for a specific class."""
        query = f'SELECT COUNT(*) FROM {self.table_name} WHERE class_name = ?'
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (object_class,))
                result = cursor.fetchone()
                total_objects = result[0] if result else 0
                app_logger.info(f"Total {object_class} objects found: {total_objects}")
                return total_objects
        except Exception as e:
            app_logger.error(f"Error retrieving total objects for class {object_class}: {str(e)}")
            return 0

    def query_objects_by_class(self, object_class):
        """Query objects by class_name and return a pandas DataFrame."""
        query = f'SELECT * FROM {self.table_name} WHERE class_name = ?'
        try:
            with self._connect() as conn:
                df = pd.read_sql(query, conn, params=(object_class,))
                app_logger.info(f"Query successful for objects of class {object_class}, returned {len(df)} rows.")
                return df  
        except Exception as e:
            app_logger.error(f"Error querying objects for class {object_class}: {str(e)}")
            return pd.DataFrame()

    def close(self):
        """Close the database connection when the app is closed."""
        try:
            if self._connect():
                self._connect().close()
                app_logger.info("Database connection has been closed.")
        except Exception as e:
            app_logger.error(f"Error closing the database connection: {str(e)}")
