from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API is Running!"

# --- नया प्रॉक्सी रूट जो थंबनेल फिक्स करेगा ---
@app.route('/proxy_image')
def proxy_image():
    img_url = request.args.get('url')
    if not img_url:
        return "No URL provided", 400
    
    # इंस्टाग्राम से इमेज डेटा फेच करना
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    img_data = requests.get(img_url, headers=headers).content
    return Response(img_data, mimetype="image/jpeg")

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
            
            # थंबनेल को प्रॉक्सी के जरिए भेजेंगे ताकि वो लोड हो सके
            raw_thumb = info.get('thumbnail')
            # अपनी Render URL यहाँ बदलें (जैसे https://insta-api-3.onrender.com)
            proxy_thumb = f"https://insta-api-3.onrender.com/proxy_image?url={raw_thumb}"

            video_data = {
                "title": info.get('title', 'Instagram Video'),
                "thumbnail": proxy_thumb, # अब यह लोड होगा
                "download_url": info.get('url'),
            }
            return jsonify(video_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
