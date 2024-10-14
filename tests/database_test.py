import unittest
import sqlite3
import datetime
from unittest.mock import MagicMock
from hawk_stream.database import DB 
from hawk_stream.detected_object import DetectedObject 

class TestDB(unittest.TestCase):

    def setUp(self):
        # Initialize DB with a test database path
        self.db = DB(db_path='tests/db_test.db')

        # Connect to the test database and create tables
        self.db.connection = sqlite3.connect(self.db.db_path)
        self.db.cursor = self.db.connection.cursor()
        self.db._create_tables()

        # Create a mock DetectedObject for testing
        self.mock_object = DetectedObject(
            object_id=1,
            first_detected_time="2024-10-14T12:00:00",
            last_detected_time="2024-10-14T12:05:00",
            class_name="Person",
            class_id=1
        )

    def tearDown(self):
        # Close the connection and remove the test database after tests
        self.db.connection.close()

    def test_create_tables(self):
        # Ensure the tables were created
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.db.cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        self.assertIn('objects', table_names)
        self.assertIn('object_counts', table_names)

    def test_add_object(self):
        # Add the mock object to the DB
        self.db.object_type = "objects"  # Mock object type
        self.db.add_object(self.mock_object)

        # Verify the object was added
        self.db.cursor.execute('SELECT * FROM objects WHERE object_id = ?', (self.mock_object.object_id,))
        result = self.db.cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], self.mock_object.object_id)
        self.assertEqual(result[2], self.mock_object.first_detected_time)
        self.assertEqual(result[3], self.mock_object.last_detected_time)
        self.assertEqual(result[4], self.mock_object.class_name)

    def test_update_last_detected(self):
        # Add the object first
        self.db.object_type = "objects"
        self.db.add_object(self.mock_object)

        # Update last detected time for the object
        new_time = datetime.datetime.now(datetime.timezone.utc).replace(second=0, microsecond=0)  # Ignore seconds and microseconds
        self.mock_object.last_detected_time = new_time.isoformat()
        self.db.update_object(self.mock_object)

        # Verify the last detected time is updated
        self.db.cursor.execute('SELECT last_detected_time FROM objects WHERE object_id = ?', (self.mock_object.object_id,))
        result = self.db.cursor.fetchone()

        result_time = datetime.datetime.fromisoformat(result[0]).replace(second=0, microsecond=0)  # Ignore seconds and microseconds
        self.assertEqual(result_time, new_time)

    def test_get_total_objects(self):
        # Insert two mock objects of the same class
        self.db.object_type = "objects"
        self.db.add_object(self.mock_object)

        another_object = DetectedObject(
            object_id=2,
            first_detected_time="2024-10-14T12:10:00",
            last_detected_time="2024-10-14T12:15:00",
            class_name="Person",
            class_id=1
        )
        self.db.add_object(another_object)

        # Verify the total count of objects of class "Person"
        total_objects = self.db.get_total_objects("Person")
        self.assertEqual(total_objects, 2)

if __name__ == '__main__':
    unittest.main()
