from fastapi import FastAPI
from mosquitto import mosquitto

message_received = []

app = FastAPI()

def handle_message(payload):
    message_received.append(payload)
    print("✅ Callback executado com mensagem:", payload)

def handle_message_test(payload):
    message_received.append(payload)
    print("procesando no banco de dados: ", payload)


@app.on_event("startup")
async def startup_event():
    mosquitto.subscribe("test/topic", handle_message)
    mosquitto.subscribe("db/test", handle_message_test)



@app.get("/")
async def root():
    return {"message": "Hello World", "message_received": message_received}