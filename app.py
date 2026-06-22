from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.websockets import WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from manager import WebSocketManager

app = FastAPI()

# Mount static assets (css, js)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # <-- Change to specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

manager = WebSocketManager()

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_json()
            print("Received message", message)
            for client in manager.connected_clients:
                await manager.send_message(client, websocket.client.host, websocket.client.port, message)
    except Exception as e:
        print("WebSocket disconnect", e)
    finally:
        await manager.disconnect(websocket)
