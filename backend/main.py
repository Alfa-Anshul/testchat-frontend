import base64, os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

_dir = os.path.dirname(os.path.abspath(__file__))
def _load():
    parts = []
    for i in range(1, 5):
        with open(os.path.join(_dir, f'parts/p{i}.txt')) as f:
            parts.append(f.read().strip())
    return base64.b64decode(''.join(parts).encode()).decode('utf-8')

HTML = _load()

@app.get('/{full_path:path}')
async def serve(full_path: str):
    return HTMLResponse(content=HTML)
