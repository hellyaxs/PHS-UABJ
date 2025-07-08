from datetime import datetime
from src.domain.models.enums.status_de_uso import StatusUsoEquipamento
from src.domain.models.equipamento import Equipamento
from src.domain.models.funcionario import Funcionario
from src.domain.models.usoequipamento import UsoEquipamento
from src.domain.models.tags import Tag
from src.infra.api.websocket.card_socket import send_message_to_clients
from src.infra.config.database.database import get_db
import json


async def handle_message(payload):
    await send_message_to_clients(payload)

async def handler_locacao_equipamento(payload):
    print("procesando no banco de dados: ", payload)
    if isinstance(payload, str):
        payload = json.loads(payload)
    
    db = next(get_db())
    # Busca o funcionário pelo código do cartão
    funcionario = db.query(Funcionario).filter(Funcionario.codigo_cartao == payload["professor_uid"]).first()
    if not funcionario:
        raise Exception(f"Funcionário não encontrado com o código do cartão: {payload['professor_uid']}")
    
    # Busca as tags e seus equipamentos associados
    tags = db.query(Tag).filter(Tag.rfid.in_(payload["projetores"])).all()
    if not tags:
        raise Exception(f"Nenhuma tag encontrada com os RFIDs: {payload['projetores']}")
    
    # Cria registros de uso para cada equipamento encontrado
    for tag in tags:
        if not tag.equipamento_codigo:
            print(f"Aviso: Tag {tag.rfid} não está associada a nenhum equipamento")
            continue
            
        equipamento = db.query(Equipamento).filter(Equipamento.codigo_tombamento == tag.equipamento_codigo).first()
        if not equipamento:
            print(f"Aviso: Equipamento não encontrado para a tag {tag.rfid}")
            continue
        if payload["acao"] == "locacao":    
            novo_uso_equipamento = UsoEquipamento(
                equipamento_codigo=equipamento.codigo_tombamento,
                funcionario_id=funcionario.id,
                data_aluguel=datetime.strptime(payload['data_hora'], '%Y-%m-%d %H:%M:%S'),
                funcionario=funcionario,
                equipamento=equipamento,
                status=StatusUsoEquipamento.ALOCADO
            )
            db.add(novo_uso_equipamento)
        else:
            # Busca o último uso do equipamento para o professor
            uso = (
                db.query(UsoEquipamento)
                .filter(
                    UsoEquipamento.equipamento_codigo == equipamento.codigo_tombamento,
                    UsoEquipamento.funcionario_id == funcionario.id
                )
                .order_by(UsoEquipamento.data_aluguel.desc())
                .first()
            )

            if uso:
                uso.data_devolucao = datetime.now()
                db.commit()
                db.refresh(uso)
    db.commit()




