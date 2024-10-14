import datetime


class DetectedObject:
    def __init__(self, object_id, class_name, class_id, first_detected_time=None, last_detected_time=None):
        self.object_id = object_id
        self.class_name = class_name
        self.class_id = class_id
        self.first_detected_time = first_detected_time or datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.last_detected_time = last_detected_time or self.first_detected_time
