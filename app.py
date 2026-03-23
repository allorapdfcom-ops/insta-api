from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Frontend को Backend से कनेक्ट करने के लिए जरूरी है

@app.route('/')
def home():
    return "Instagram Downloader API is Running!"

@app.route('/get_video', methods=['POST'])
def get_video():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "URL is required"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_data = {
                "title": info.get('title', 'Instagram Video'),
                "thumbnail": info.get('thumbnail'),
                "download_url": info.get('url'),
                "duration": info.get('duration_string')
            }
            return jsonify(video_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
