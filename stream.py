# import os
# import subprocess
# import datetime
# from flask import Flask, jsonify, send_file

# app = Flask(__name__)

# YOUTUBE_STREAM_KEY = 'q85g-440x-hx46-jwsj-f85q'

# if not YOUTUBE_STREAM_KEY:
#     print("Error: YouTube stream key is not set.")
#     exit(1)

# VIDEO_PATH = "cat.mp4"

# ffmpeg_command = f"""
# ffmpeg -re -stream_loop -1 -i {VIDEO_PATH} -vcodec libx264 -pix_fmt yuv420p -preset veryfast -maxrate 3000k -bufsize 6000k -acodec aac -ar 44100 -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}
# """

# stream_start_time = datetime.datetime.utcnow()

# @app.route('/health', methods=['GET'])
# def health_check():
#     return "OK", 200

# @app.route('/api/stream', methods=['GET'])
# def stream_status():
#     return jsonify({
#         "start_time": stream_start_time.isoformat() + "Z"
#     })

# @app.route('/')
# def index():
#     return send_file('index.html')

# if __name__ == '__main__':
#     process = subprocess.Popen(ffmpeg_command, shell=True)
#     app.run(host='0.0.0.0', port=10000)











import os
from flask import Flask, jsonify
from datetime import datetime
import threading

app = Flask(__name__)

# Fetch the stream keys from environment variables
YOUTUBE_STREAM_KEY = os.getenv("YOUTUBE_STREAM_KEY")
FACEBOOK_STREAM_KEY = os.getenv("FACEBOOK_STREAM_KEY")

# Check if the stream keys are available
if not YOUTUBE_STREAM_KEY or not FACEBOOK_STREAM_KEY:
    print("Error: Environment variables for YouTube or Facebook stream keys are not set.")
    exit(1)

# Set the video file path
VIDEO_PATH = "cat.mp4"  # Ensure the file exists and has the correct path

# FFmpeg command templates
youtube_command = f"""
ffmpeg -re -stream_loop -1 -i {VIDEO_PATH} -vcodec libx264 -pix_fmt yuv420p -preset veryfast -maxrate 3000k -bufsize 6000k -acodec aac -ar 44100 -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}
"""

facebook_command = f"""
ffmpeg -re -stream_loop -1 -i {VIDEO_PATH} -vcodec libx264 -pix_fmt yuv420p -preset veryfast -maxrate 3000k -bufsize 6000k -acodec aac -ar 44100 -b:a 128k -f flv rtmp://live-api-s.facebook.com:443/rtmp/{FACEBOOK_STREAM_KEY}
"""

# Function to run FFmpeg command
def start_stream(command):
    os.system(command)

# Start streams in separate threads
def start_streams():
    youtube_thread = threading.Thread(target=start_stream, args=(youtube_command,))
    facebook_thread = threading.Thread(target=start_stream, args=(facebook_command,))
    youtube_thread.start()
    facebook_thread.start()

@app.route('/api/stream', methods=['GET'])
def stream_status():
    start_time = datetime.now().isoformat()
    return jsonify({'start_time': start_time})

if __name__ == '__main__':
    start_streams()
    app.run()
