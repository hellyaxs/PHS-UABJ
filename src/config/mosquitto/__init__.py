from .mosquito import MosquittoClient
from src.config.settings import mqtt_settings
import asyncio


loop = asyncio.get_event_loop()

mosquitto = MosquittoClient(broker=mqtt_settings.MQTT_BROKER, port=mqtt_settings.MQTT_PORT)
mosquitto.set_event_loop(loop)

