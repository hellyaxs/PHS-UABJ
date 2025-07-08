from enum import Enum

class StatusUsoEquipamento(str, Enum):
    ALOCADO = "ALOCADO"
    DEVOLVIDO = "DEVOLVIDO"
    DEVOLVIDO_DEFEITO = "DEVOLVIDO COM DEFEITO"
    EM_USO = "EM_USO"
    PENDENTE = "PENDENTE"
    EMAIL_ENVIADO = "EMAIL_ENVIADO"

class StatusTag(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"