from .user_controller import user_router
from .equipamento_controller import equipamento_router
from .defeito_controller import defeito_router
from .curso_controller import curso_router
from .funcionario_controller import funcionario_router
from .cartao_controller import  router_cartao
from .uso_equipamento_controller import locacao_router

all_routers = [
    user_router,
    equipamento_router,
    defeito_router,
    curso_router,
    funcionario_router,
    router_cartao,
    locacao_router,
]