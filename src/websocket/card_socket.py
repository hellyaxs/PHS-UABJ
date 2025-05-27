
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

active_connections: List[WebSocket] = []

@router.websocket("/addcard")
async def websocket_addcard_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"Cliente conectado (via router) a /addcard: {websocket.client}")

    await websocket.send_text("Você está inscrito para receber atualizações de 'addcard' (via router).")
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"Cliente desconectado (via router) a /addcard: {websocket.client}")


     