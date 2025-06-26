
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from src.infra.config.mosquitto import mosquitto

router = APIRouter()

active_connections: List[WebSocket] = []

@router.websocket("/add")
async def websocket_addcard_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"Cliente conectado (via router) a /add: {websocket.client}")

    await websocket.send_text("Você está inscrito para receber atualizações de 'add' (via router).")
    try:
        while True:
            data = await websocket.receive_text()
            send_message_to_mosquitto(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"Cliente desconectado (via router) a /add: {websocket.client}")


def send_message_to_mosquitto(message: str):
    mosquitto.publish("add", message)