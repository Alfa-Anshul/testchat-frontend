from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Serve built React app
if os.path.exists('dist'):
    app.mount('/assets', StaticFiles(directory='dist/assets'), name='assets')

    @app.get('/{full_path:path}')
    async def serve_spa(full_path: str):
        return FileResponse('dist/index.html')
else:
    @app.get('/')
    async def root():
        return {'status': 'building', 'message': 'React build not found. Run npm run build first.'}
