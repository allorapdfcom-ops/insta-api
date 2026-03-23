from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import yt_dlp
import httpx
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared HTTPX Client for better performance
client = httpx.AsyncClient(timeout=10.0)

@app.get("/")
async def home():
    return {"status": "ok", "msg": "Lite API"}

@app.get("/download")
async def get_info(url: str):
    # Minimal options to save RAM/CPU
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'no_playlist': True,
        'skip_download': True,
        'format': 'best',
    }
    
    try:
        # Run yt_dlp in a thread to not block the event loop
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
            
            return {
                "status": "success",
                "title": info.get('title', 'Video'),
                "description": info.get('description', '')[:100], # Limit description size
                "thumbnail": info.get('thumbnail'),
                "download_url": info.get('url'),
                "like_count": info.get('like_count', 'N/A'),
                "comment_count": info.get('comment_count', 'N/A')
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Link or Server Busy")

@app.get("/proxy-download")
async def proxy_download(url: str):
    try:
        # Efficient streaming without loading file into RAM
        async def stream_video():
            async with client.stream("GET", url) as response:
                async for chunk in response.aiter_bytes(chunk_size=1024*64): # 64KB chunks
                    yield chunk

        return StreamingResponse(
            stream_video(),
            media_type="video/mp4",
            headers={"Content-Disposition": "attachment; filename=video.mp4"}
        )
    except:
        raise HTTPException(status_code=500, detail="Proxy failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
