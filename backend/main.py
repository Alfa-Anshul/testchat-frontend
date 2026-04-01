from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = open("standalone.html").read() if __import__("os").path.exists("standalone.html") else "<h1>Building...</h1>"

@app.get("/{full_path:path}")
async def serve(full_path: str):
    return HTMLResponse(content=open("standalone.html").read() if __import__("os").path.exists("standalone.html") else HTML)
