import cv2
from datetime import datetime
import time
from typing import Set
from object_detector import ObjectDetector
from stream_insight import StreamInsight
from detected_object import DetectedObject
class FrameProcessor:
    def __init__(self,is_detection=True,is_record=True, is_timestamp=False):
        self.object_detector=ObjectDetector() if is_detection else None 
        self.stream_insight=StreamInsight()if is_detection else None 
        self.is_record=is_record
        self.is_timestamp=is_timestamp
        self.last_cleanup_time = time.time()  # Track the last time cleanup was triggered
        self.cleanup_interval = 5  # Cleanup every 5 seconds
        # Font settings for annotations
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_color = (255, 255, 255)  # White color
        self.font_thickness = 2
        self.font_line_type = cv2.LINE_AA 

    
    def process(self,frame):
        if self.object_detector:
            frame, active_objects =self.object_detector.detect_and_track(frame)
            if self.is_record:
                self.upsert_object(active_objects)      
        current_time = time.time()
        if current_time - self.last_cleanup_time >= self.cleanup_interval:
            self.stream_insight.remove_inactive_objects()
            self.last_cleanup_time = current_time  # Reset the last cleanup time

        if self.is_timestamp:
            frame=self.add_timestamp(frame)
        return frame
    
    def upsert_object(self, active_objects: Set[DetectedObject]):
        for obj in active_objects:
            object_key = f"{obj.class_id}_{obj.object_id}"
            if object_key not in self.stream_insight.active_objects:
                self.stream_insight.add_object(obj)
            else:
                self.stream_insight.update_object(obj)




    def add_timestamp(self, frame):
        """Add a timestamp to the bottom-left corner of the frame."""
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Get the dimensions of the frame
        height, width, _ = frame.shape
        # Set the position of the timestamp
        text_size, _ = cv2.getTextSize(timestamp, self.font, self.font_scale, self.font_thickness)
        text_width, text_height = text_size
        x = 10  # 10 pixels from the left
        y = height - 10  # 10 pixels from the bottom
        # Add text to the frame
        cv2.putText(frame, timestamp, (x, y), self.font, self.font_scale,
                    self.font_color, self.font_thickness, self.font_line_type)
        return frame