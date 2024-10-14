from flask import Flask, Response
from stream import Stream

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    stream=Stream()
    return Response(stream.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5005, debug=True, threaded=True)
    finally:
        print("Closing App")