import torch
import supervision as sv
from ultralytics import YOLO
from logger import app_logger
from config import YOLO_MODEL 
from detected_object import DetectedObject
# To run on Mac: Check if MPS is available
if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
app_logger.info(f"{device} is used for torch compute")
class ObjectDetector:
    def __init__(self, model_name=YOLO_MODEL):
        self.model = YOLO(model_name)
        self.model.fuse() 
        self.tracker = sv.ByteTrack()
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
    
    def detect_and_track(self, frame):
        results = self.model.predict(frame, imgsz=640, conf=0.5, verbose=False)
        detections = results[0]
        
        converted_detections = sv.Detections.from_ultralytics(detections)
        
        tracked_detections = self.tracker.update_with_detections(converted_detections)
        
        labels = []
        active_objects=set()
        for class_id, tracker_id in zip(tracked_detections.class_id, tracked_detections.tracker_id):
            class_name = detections.names[class_id]
            object=DetectedObject(tracker_id,class_name,class_id)
            active_objects.add(object)
            label = f"#{tracker_id} {class_name}"
            labels.append(label)

        
        annotated_frame = self.box_annotator.annotate(scene=frame.copy(), detections=tracked_detections)
        
        annotated_frame = self.label_annotator.annotate(scene=annotated_frame, detections=tracked_detections, labels=labels)
        
        return annotated_frame , active_objects
