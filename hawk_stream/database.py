from datetime import datetime, timezone
import sqlite3 
from config import DATABASE
from detected_object import DetectedObject

class DB:
    def __init__(self, db_path=DATABASE):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path) 
        self.cursor = self.connection.cursor() 
        self.table_name = "objects"
        self._create_tables()  # Call table creation here
           
    def _create_tables(self):
        # Correct string interpolation for table name
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                object_id INTEGER UNIQUE,
                first_detected_time TEXT,
                last_detected_time TEXT,
                class_name TEXT,
                class_id INTEGER
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS object_counts (
                timestamp TEXT PRIMARY KEY,
                count INTEGER NOT NULL
            )
        ''')
        
        self.connection.commit()

    def add_object(self, detected_object: DetectedObject):
        if detected_object.object_id is None:
            print(f"Warning: {detected_object.object_id} is None, skipping add_object")
            return
        
        # Insert or ignore if object already exists
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO {self.table_name} (object_id, first_detected_time, last_detected_time, class_name, class_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (detected_object.object_id, detected_object.first_detected_time, detected_object.last_detected_time, detected_object.class_name, detected_object.class_id))
        
        # Update last_detected_time if the object already exists
        self.cursor.execute(f'''
            UPDATE {self.table_name}
            SET last_detected_time = ?
            WHERE object_id = ?
        ''', (detected_object.last_detected_time, detected_object.object_id))
        
        self.connection.commit()
    
    def update_object(self, detected_object: DetectedObject):
        if detected_object.object_id is None:
            print(f"Warning: {detected_object.object_id} is None, skipping update_object")
            return
        
        # Use the last_detected_time from the DetectedObject to update the entry
        self.cursor.execute(f'''
            UPDATE {self.table_name}
            SET last_detected_time = :last_detected_time
            WHERE object_id = :object_id
        ''', {
            'last_detected_time': detected_object.last_detected_time,
            'object_id': detected_object.object_id
        })

        self.connection.commit()

    def get_total_objects(self, object_class):
        # Get total number of unique objects detected for a specific class
        query = f'SELECT COUNT(*) FROM {self.table_name} WHERE class_name = ?'
        self.cursor.execute(query, (object_class,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def close(self):
        """Close the connection to the database"""
        self.connection.close()
