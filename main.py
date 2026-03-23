from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import instaloader
import os

app = FastAPI()

# CORS settings for Hostinger Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # अपनी Hostinger डोमेन यहाँ डालें
    allow_methods=["*"],
    allow_headers=["*"],
)

L = instaloader.Instaloader()

@app.get("/")
def home():
    return {"message": "Instagram Downloader API is Running"}

@app.get("/fetch")
def fetch_insta_data(url: str):
    try:
        # Extract shortcode from URL
        if "reels/" in url or "p/" in url:
            shortcode = url.split("/")[-2]
        else:
            shortcode = url.split("/")[-1]

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Video/Image Details
        data = {
            "caption": post.caption,
            "likes": post.likes,
            "comments": post.comments,
            "is_video": post.is_video,
            "display_url": post.display_url, # Thumbnail
            "download_url": post.video_url if post.is_video else post.url,
            "owner": post.owner_username
        }
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid URL or Private Post")

# Note: Stories ke liye login session lagta hai jo Render par file save karke hota hai.
# Filhal ye Reels aur Posts ke liye best hai.
