from flask import Flask, request, jsonify, send_file
import yt_dlp as youtube_dl
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    resolution = data.get('resolution')

    ydl_opts = {
        'format': f'best[height<={resolution}]',
        'outtmpl': 'downloaded_video.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return jsonify({'file_url': '/downloaded_video.mp4'})

@app.route('/downloaded_video.mp4')
def get_video():
    return send_file('downloaded_video.mp4')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
