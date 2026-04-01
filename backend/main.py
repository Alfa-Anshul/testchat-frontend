import os
import subprocess
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ---- Build React if dist is missing ----
if not os.path.exists('dist'):
    print('[startup] dist/ not found — running npm install && npm run build ...', flush=True)
    r1 = subprocess.run(['npm', 'install'], check=True)
    r2 = subprocess.run(['npm', 'run', 'build'], check=True)
    print('[startup] Build complete.', flush=True)

app = FastAPI()

# Mount static assets
app.mount('/assets', StaticFiles(directory='dist/assets'), name='assets')

@app.get('/{full_path:path}')
async def serve_spa(full_path: str):
    return FileResponse('dist/index.html')
