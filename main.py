from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS allow (frontend connect karega)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

def get_shortcode(url):
    match = re.search(r"instagram.com/(?:p|reel|tv)/([^/?]+)", url)
    return match.group(1) if match else None

@app.get("/")
def home():
    return {"status": "API Running 🚀"}

@app.post("/api")
def fetch_data(req: URLRequest):
    try:
        shortcode = get_shortcode(req.url)
        if not shortcode:
            return {"error": "Invalid URL"}

        api_url = f"https://www.instagram.com/p/{shortcode}/?__a=1&__d=dis"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(api_url, headers=headers)
        data = res.json()

        media = data["graphql"]["shortcode_media"]

        return {
            "thumbnail": media["display_url"],
            "caption": media["edge_media_to_caption"]["edges"][0]["node"]["text"] if media["edge_media_to_caption"]["edges"] else "",
            "likes": media["edge_media_preview_like"]["count"],
            "download": media.get("video_url") or media["display_url"]
        }

    except Exception as e:
        return {"error": str(e)}
