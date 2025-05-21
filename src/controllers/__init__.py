from .user_controller import user_router
from .equipamento_controller import equipamento_router
from .defeito_controller import defeito_router
from .curso_controller import curso_router

all_routers = [
    user_router,
    equipamento_router,
    defeito_router,
    curso_router,
]