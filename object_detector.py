import torch
import supervision as sv
from ultralytics import YOLO
from config import YOLO_MODEL
# To run on Mac: Check if MPS is available
if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print(device)

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
        for class_id, tracker_id in zip(tracked_detections.class_id, tracked_detections.tracker_id):
            class_name = detections.names[class_id]
            label = f"#{tracker_id} {class_name}"
            labels.append(label)

        
        annotated_frame = self.box_annotator.annotate(scene=frame.copy(), detections=tracked_detections)
        
        annotated_frame = self.label_annotator.annotate(scene=annotated_frame, detections=tracked_detections, labels=labels)
        
        return annotated_frame
