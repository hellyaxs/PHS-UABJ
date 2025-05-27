message_received = []

from src.websocket.card_socket import active_connections

async def send_message_to_clients(message: str):
    """
    Sends a message to all active WebSocket connections.
    """
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Error sending message to client: {e}")


async def handle_message(payload):
    message_received.append(payload)
    print("✅ Callback executado com mensagem:", payload)
    await send_message_to_clients(payload)

async def handle_message_test(payload):
    message_received.append(payload)
    print("procesando no banco de dados: ", payload)
    await send_message_to_clients(payload)