from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import yt_dlp
import requests
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Insta Downloader API is Running!"}

@app.get("/download")
def get_video_info(url: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extracting details
            return {
                "status": "success",
                "title": info.get('title', 'Instagram Video'),
                "description": info.get('description', 'No caption available'),
                "thumbnail": info.get('thumbnail'),
                "download_url": info.get('url'),
                "like_count": info.get('like_count', 'N/A'),
                "comment_count": info.get('comment_count', 'N/A'),
                "view_count": info.get('view_count', 'N/A')
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Proxy Endpoint for Direct Download
@app.get("/proxy-download")
def proxy_download(url: str = Query(...), filename: str = "instagram_video.mp4"):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Headers to force download
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'video/mp4'
        }
        
        return StreamingResponse(response.iter_content(chunk_size=1024*1024), headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not download video")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
