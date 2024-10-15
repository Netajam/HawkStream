from flask import Flask, Response, render_template, jsonify, request
from logger import app_logger
from stream import Stream
from data_visualization import DataVisualization

app = Flask(__name__)

visualization = DataVisualization()
stream=Stream()

@app.errorhandler(Exception)
def handle_exception(e):
    app_logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(stream.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/cumulative_affluence_data')
def cumulative_affluence_data():

    object_type = request.args.get('object_type', 'car')
    time_range = int(request.args.get('time_range', 6))  
    df = visualization.fetch_data(object_class=object_type, hours_in_past=time_range)
    return visualization.cumulative_affluence_json(df)

@app.route('/api/instantaneous_affluence_data')
def instantaneous_affluence_data():

    object_type = request.args.get('object_type', 'car')
    time_range = int(request.args.get('time_range', 6))  
    df = visualization.fetch_data(object_class=object_type, hours_in_past=time_range)
    return visualization.instantaneous_affluence_json(df, interval='15T')


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5005, debug=True, threaded=True)
    finally:
        app_logger.info("Closing App")
        stream.close()
