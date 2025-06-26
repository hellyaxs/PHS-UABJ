from enum import Enum

class StatusUsoEquipamento(str, Enum):
    ALOCADO = "ALOCADO"
    DEVOLVIDO = "DEVOLVIDO"
    EM_USO = "EM_USO"
    PENDENTE = "PENDENTE"

class StatusTag(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"