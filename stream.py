import os
import subprocess
import datetime
from flask import Flask, jsonify, send_file

app = Flask(__name__)

YOUTUBE_STREAM_KEY = 'q85g-440x-hx46-jwsj-f85q'

if not YOUTUBE_STREAM_KEY:
    print("Error: YouTube stream key is not set.")
    exit(1)

VIDEO_PATH = "cat.mp4"

ffmpeg_command = f"""
ffmpeg -re -stream_loop -1 -i {VIDEO_PATH} -vcodec libx264 -pix_fmt yuv420p -preset veryfast -maxrate 3000k -bufsize 6000k -acodec aac -ar 44100 -b:a 128k -f flv rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}
"""

stream_start_time = datetime.datetime.utcnow()

@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

@app.route('/api/stream', methods=['GET'])
def stream_status():
    return jsonify({
        "start_time": stream_start_time.isoformat() + "Z"
    })

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == '__main__':
    process = subprocess.Popen(ffmpeg_command, shell=True)
    app.run(host='0.0.0.0', port=10000)
