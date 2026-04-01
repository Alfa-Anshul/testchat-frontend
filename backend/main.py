from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Mount static assets (pre-built React dist is committed to the repo)
app.mount('/assets', StaticFiles(directory='dist/assets'), name='assets')

@app.get('/{full_path:path}')
async def serve_spa(full_path: str):
    return FileResponse('dist/index.html')
