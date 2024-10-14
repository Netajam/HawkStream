from config import CAMERA_SRC2
from camera import Camera
import cv2

class Stream:
    def __init__(self, camera: Camera = Camera(CAMERA_SRC2)):
        self.camera = camera

    def generate_frames(self):
        while True:
            frame = self.camera.get_frame()
            if frame is None:
                continue
            yield frame

if __name__ == '__main__':
    stream = Stream()
    frame_generator = stream.generate_frames()

    for frame in frame_generator:
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
