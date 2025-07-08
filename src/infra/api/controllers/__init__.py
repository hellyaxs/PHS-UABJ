from src.infra.api.controllers.auth_controller import router_auth
from .equipamento_controller import equipamento_router
from .defeito_controller import defeito_router
from .curso_controller import curso_router
from .funcionario_controller import funcionario_router
from .cartao_controller import  router_cartao
from .uso_equipamento_controller import locacao_router
from .cargo_controller import router_cargo
from .tag_controller import tag_router

all_routers = [
    router_auth
]

protected_routers = [
    equipamento_router,
    defeito_router,
    curso_router,
    funcionario_router,
    router_cartao,
    locacao_router, 
    router_cargo,
    tag_router,
]