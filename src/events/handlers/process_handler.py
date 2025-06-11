from datetime import datetime
from src.models.enums.status_de_uso import StatusUsoEquipamento
from src.models.equipamento import Equipamento
from src.models.funcionario import Funcionario
from src.models.usoequipamento import UsoEquipamento
from src.models.tags import Tag
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
    
    # Busca o funcionário pelo código do cartão
    funcionario = db.query(Funcionario).filter(Funcionario.codigo_cartao == payload["codigo_cartao"]).first()
    if not funcionario:
        raise Exception(f"Funcionário não encontrado com o código do cartão: {payload['codigo_cartao']}")
    
    # Busca as tags e seus equipamentos associados
    tags = db.query(Tag).filter(Tag.rfid.in_(payload["tags"])).all()
    if not tags:
        raise Exception(f"Nenhuma tag encontrada com os RFIDs: {payload['tags']}")
    
    # Cria registros de uso para cada equipamento encontrado
    for tag in tags:
        if not tag.equipamento_codigo:
            print(f"Aviso: Tag {tag.rfid} não está associada a nenhum equipamento")
            continue
            
        equipamento = db.query(Equipamento).filter(Equipamento.codigo_tombamento == tag.equipamento_codigo).first()
        if not equipamento:
            print(f"Aviso: Equipamento não encontrado para a tag {tag.rfid}")
            continue
            
        novo_uso_equipamento = UsoEquipamento(
            equipamento_codigo=equipamento.codigo_tombamento,
            funcionario_id=funcionario.id,
            data_aluguel=datetime.now(),
            funcionario=funcionario,
            equipamento=equipamento,
            status=StatusUsoEquipamento.ALOCADO
        )
        db.add(novo_uso_equipamento)
    
    db.commit()



