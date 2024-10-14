from config import CAMERA_SRC2
from camera import Camera
import cv2

from frame_processor import FrameProcessor
class Stream:
    def __init__(self, camera: Camera = Camera(CAMERA_SRC2),is_detection=True):
        self.camera = camera
        self.frame_processor=FrameProcessor(is_detection,True)
        self.is_detection=is_detection

    def generate_raw_frames(self):
        while True:
            frame = self.camera.get_frame()
            if frame is None:
                continue
            yield frame

    def generate_frames(self):
        while True:
            frame = self.camera.get_frame()
            if frame is None:
                break

            frame=self.frame_processor.process(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    stream = Stream()
    frame_generator = stream.generate_raw_frames()

    for frame in frame_generator:
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
