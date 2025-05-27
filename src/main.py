from fastapi import FastAPI
from src.controllers import all_routers
from src.config.mosquitto import mosquitto
from src.events.handlers.process_handler import handle_message
from src.config.settings import app_settings
from fastapi.middleware.cors import CORSMiddleware
from src.websocket.card_socket import router as websocket_route

app = FastAPI(
    title=app_settings.PROJECT_NAME,
    debug=app_settings.DEBUG
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

[app.include_router(router) for router in all_routers]
app.include_router(websocket_route)


@app.on_event("startup")
async def startup_event():    
    mosquitto.subscribe("db/test", handle_message)
    mosquitto.subscribe("possiveis_erros", handle_message)

@app.on_event("shutdown")
async def shutdown_event():
    pass
