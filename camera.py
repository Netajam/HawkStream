# camera.py
import cv2

class Camera:
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.video = cv2.VideoCapture(self.stream_url)
        if not self.video.isOpened():
            raise Exception(f"Could not open video stream from {self.stream_url}")

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            self.video = cv2.VideoCapture(self.stream_url)
            return None
        return frame  
