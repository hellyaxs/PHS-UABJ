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
            # Mantém a conexão ativa sem processar dados recebidos
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"Cliente desconectado (via router) a /add: {websocket.client}")

@router.websocket("/newuso")
async def websocket_newuso_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"Cliente conectado (via router) a /newuso: {websocket.client}")
    try:
        while True:
            # Mantém a conexão ativa sem processar dados recebidos
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"Cliente desconectado (via router) a /newuso: {websocket.client}")
    



async def send_message_to_clients(message: str):
    """
    Sends a message to all active WebSocket connections.
    """
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Error sending message to client: {e}")