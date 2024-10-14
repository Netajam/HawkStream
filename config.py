import os
from dotenv import load_dotenv

load_dotenv()

CAMERA_SRC1 = '/dev/video0'
rtsp_password = os.getenv('RTSP_PASSWORD')
rtsp_admin= os.getenv('RTSP_ADMIN')
rtsp_ip= os.getenv('RTSP_IP')
CAMERA_SRC2 = f'rtsp://{rtsp_admin}:{rtsp_password}@{rtsp_ip}/stream1'
CAMERA_SRC2_1 = f'rtsp://{rtsp_admin}:{rtsp_password}@{rtsp_ip}/stream2'
DATABASE='object_detection.db'