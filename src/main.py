from fastapi import Depends, FastAPI
from src.infra.config.security.cors import configure_cors
from src.infra.config.security.jwt import get_current_user
from src.infra.api.controllers import all_routers, protected_routers
from src.infra.config.mosquitto import mosquitto
from src.domain.events.handlers.process_handler import handle_message, handler_locacao_equipamento
from src.infra.config.settings import app_settings
from src.infra.api.websocket.card_socket import router as websocket_route
from src.infra.config.cron.jobs import start_scheduler, stop_scheduler
from src.infra.config.database.database import Base, engine
from src.domain.models import *

Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title=app_settings.PROJECT_NAME,
    debug=app_settings.DEBUG,
)

# CORS
configure_cors(app)

#Rotas Públicas
[app.include_router(router) for router in all_routers]
app.include_router(websocket_route)

# Rotas protegidas por autenticação
for router in protected_routers:
    app.include_router(router, dependencies=[Depends(get_current_user)])


@app.on_event("startup")
async def startup_event():    
    # Passa as funções diretamente, sem executá-las
    start_scheduler()
    mosquitto.subscribe("db/test", handle_message)
    mosquitto.subscribe("alocacao_equipamento", handler_locacao_equipamento)

@app.on_event("shutdown")
async def shutdown_event():
    stop_scheduler()
