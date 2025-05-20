from fastapi import FastAPI
from controllers.user_controller import user_router
from mosquitto import mosquitto
from events.handlers.process_handler import handle_message
from config.settings import app_settings
app = FastAPI(
    title=app_settings.PROJECT_NAME,
    debug=app_settings.DEBUG
)

app.include_router(user_router)

@app.on_event("startup")
async def startup_event():    
    mosquitto.subscribe("db/test", handle_message)
    mosquitto.subscribe("possiveis_erros", handle_message)

@app.on_event("shutdown")
async def shutdown_event():
    pass
