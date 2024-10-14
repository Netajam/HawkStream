# HawkStream

HawkStream applies computer vision on camera streams, allowing users to visualize annotated streams and analyze data through a web app.

## Features

- **Visualizing the annotated stream**
- **Displaying data analysis charts**
- **Object detection alerts with captured images**
- **Capturing images of detected objects and storing them in the cloud**
- **Timelapse functionality**

## Serving the Stream

- **Local Streaming** (direct access on your machine)
- **Webserver Streaming** (access via a hosted web app)

## Configuration

### Hardware

- Camera connected via USB or streaming via RTSP.
- A computer with GPU support (for optimal performance).

### Tech Stack

- **Python**
- **Flask** (for web application)
- **YOLO** (for object detection, running with PyTorch)
- **Supervision** (for object tracking)

## Getting Started

1. **Create a `.env` file**  
   Add your environment-specific variables, such as API keys, storage credentials, etc.

2. **Set up a Python virtual environment**  
   ```
   python -m venv venv
   source venv/bin/activate  # For Unix/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install the required dependencies**  
   ```
   pip install -r requirements.txt
   ```

## Additional Notes

- Make sure you have GPU drivers installed and properly configured to use YOLO with PyTorch.
- Set the necessary configuration for the camera in the `.env` file, such as RTSP URL or USB camera details.

