import os, subprocess, sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')

if not os.path.exists(DIST):
    print('[startup] Building React app...', flush=True)
    node = subprocess.run(['which', 'node'], capture_output=True).stdout.strip()
    npm = subprocess.run(['which', 'npm'], capture_output=True).stdout.strip()
    print(f'[startup] node={node} npm={npm}', flush=True)
    if npm:
        subprocess.run(['npm', 'install'], cwd=ROOT, check=True)
        subprocess.run(['npm', 'run', 'build'], cwd=ROOT, check=True)
        print('[startup] Build complete!', flush=True)
    else:
        print('[startup] npm not found — serving fallback', flush=True)

app = FastAPI()

if os.path.exists(DIST):
    app.mount('/assets', StaticFiles(directory=os.path.join(DIST, 'assets')), name='assets')

    @app.get('/{full_path:path}')
    async def serve(full_path: str):
        return FileResponse(os.path.join(DIST, 'index.html'))
else:
    @app.get('/{full_path:path}')
    async def fallback(full_path: str):
        from fastapi.responses import HTMLResponse
        return HTMLResponse('<h2 style="font-family:sans-serif;padding:40px">Building... please wait and refresh.</h2>')
