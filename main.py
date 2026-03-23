from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# CORS allow karna zaroori hai taaki frontend backend se connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Instagram Downloader API is Running!"}

@app.get("/download")
def download_video(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'instagram_video')
            thumbnail = info.get('thumbnail')

            return {
                "status": "success",
                "title": title,
                "download_url": video_url,
                "thumbnail": thumbnail
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
