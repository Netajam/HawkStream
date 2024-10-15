from typing import Dict
import datetime
from logger import app_logger
from detected_object import DetectedObject
from database import DB
class StreamInsight:
    def __init__(self):
        self.active_objects:Dict[str,DetectedObject] = {}
        self.database=DB()
    def record_object(self):
        pass 

    def add_object(self,obj:DetectedObject): 
        print("add object")
        app_logger.debug("D add objects")
        self.active_objects[f"{obj.class_id}_{obj.object_id}"]=obj
        self.database.add_object(obj)
    def update_object(self, obj: DetectedObject): 
        print("update objects")
        object_key = f"{obj.class_id}_{obj.object_id}"
        
        if object_key in self.active_objects:
            self.active_objects[object_key].last_detected_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
            self.database.update_object(self.active_objects[object_key])
        else:
            app_logger.error(f"Object with key {object_key} not found in active_objects.") 

    def remove_inactive_objects(self, timeout_seconds=5):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        
        for object_key, detected_object in list(self.active_objects.items()):
            last_seen_time = datetime.datetime.fromisoformat(detected_object.last_detected_time)
            elapsed_time = (current_time - last_seen_time).total_seconds()

            if elapsed_time > timeout_seconds:
                app_logger.info(f"Removing inactive object with key {object_key}")
                del self.active_objects[object_key]
