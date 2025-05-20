from .mosquito import MosquittoClient
from src.config.settings import mqtt_settings

mosquitto = MosquittoClient(broker=mqtt_settings.MQTT_BROKER, port=mqtt_settings.MQTT_PORT)

