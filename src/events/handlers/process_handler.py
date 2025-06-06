from datetime import datetime
from src.models.enums.status_de_uso import StatusUsoEquipamento
from src.models.equipamento import Equipamento
from src.models.funcionario import Funcionario
from src.models.usoequipamento import UsoEquipamento
from src.websocket.card_socket import active_connections
from src.config.database.database import get_db
import json
from sqlalchemy.orm import Session

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
    print("✅ Callback executado com mensagem:", payload)
    await send_message_to_clients(payload)

async def handler_locacao_equipamento(payload):
    print("procesando no banco de dados: ", payload)
    if isinstance(payload, str):
        payload = json.loads(payload)
    
    db = next(get_db())
    funcionario = db.query(Funcionario).filter(Funcionario.codigo_cartao == payload["codigo_cartao"]).first()
    equipamento = db.query(Equipamento).filter(Equipamento.codigo_tombamento == payload["codigo_tombamento"]).first()
    novo_uso_equipamento = UsoEquipamento(
        equipamento_codigo=payload["codigo_tombamento"],
        funcionario_id=funcionario.id,
        data_aluguel=payload["data_aluguel"],
        funcionario=funcionario,
        equipamento=equipamento,
        status=StatusUsoEquipamento.ALOCADO
    )
    db.add(novo_uso_equipamento)
    db.commit()
    db.refresh(novo_uso_equipamento)



