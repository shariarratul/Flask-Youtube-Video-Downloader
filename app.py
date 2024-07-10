from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    resolution = data.get('resolution')
    
    ydl_opts = {
        'format': f'best[height<={resolution}]',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info_dict)

    return jsonify({'file_url': f'/{video_file}'})

@app.route('/downloads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
