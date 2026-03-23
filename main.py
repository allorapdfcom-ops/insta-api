from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import instaloader
import uvicorn

app = FastAPI(title="InstaDownloader API")

# CORS Setup: यहाँ हमने आपके डोमेन को Allow किया है
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://allorapdf.com", "http://allorapdf.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Instaloader (Lite mode)
L = instaloader.Instaloader(
    download_pictures=False, 
    download_videos=False, 
    download_video_thumbnails=False, 
    save_metadata=False, 
    compress_json=False
)

@app.get("/")
def health_check():
    return {"status": "active", "message": "API is running for allorapdf.com/aa"}

@app.get("/fetch")
def fetch_insta_data(url: str = Query(..., description="Instagram URL")):
    try:
        # Extract shortcode
        if "reels/" in url or "p/" in url:
            shortcode = url.split("/")[-2]
        else:
            shortcode = url.split("/")[-1].split("?")[0]

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        return {
            "success": True,
            "caption": post.caption if post.caption else "No Caption",
            "likes": post.likes,
            "comments": post.comments,
            "is_video": post.is_video,
            "thumbnail": post.display_url,
            "download_url": post.video_url if post.is_video else post.url,
            "username": post.owner_username
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="पद या रील निजी (Private) है या लिंक गलत है।")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
