from enum import Enum

class StatusUsoEquipamento(str, Enum):
    ALOCADO = "Alocado"
    DEVOLVIDO = "Devolvido"
    EM_USO = "Em uso" 