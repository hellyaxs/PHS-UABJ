import paho.mqtt.client as mqtt
from typing import Callable, Dict, List
import asyncio

class MosquittoClient():
    def __init__(self, broker:str, port: int = 1883):
        self.broker = broker
        self.port = port
        self._callbacks: Dict[str, Callable[[str], None]] = {}
        self.topics: List[str] = []
        self._client = mqtt.Client(client_id="api_client", clean_session=False)
        self._client.connect(self.broker, self.port, 60)
        self._client.on_message = self._on_message
        self._loop = None
        
    def connect(self):
        if not self._client.is_connected():
            self._client.connect(self.broker, self.port, 60)
        

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if self._loop:
            self._loop.call_soon_threadsafe(self._create_task, self._callbacks[topic], payload)  # Chama o callback
        else:
            print(f"⚠️ Nenhum callback registrado para o tópico {topic}")
            
    def _create_task(self, callback, payload):
        asyncio.create_task(callback(payload))

    def set_event_loop(self, loop):
        """Set the event loop for the Mosquito instance."""
        self._loop = loop

    def publish(self, topic, payload, qos=1, retain=False):
        """
        Publica uma mensagem com QoS configurável para garantir entrega
        qos=0: At most once (sem garantia)
        qos=1: At least once (garantia de entrega, pode duplicar)
        qos=2: Exactly once (garantia de entrega única)
        """
        result = self._client.publish(topic, payload, qos=qos, retain=retain)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Erro ao publicar mensagem: {result.rc}")
        return result
    
    def subscribe(self, topic: str, callback: Callable[[str], None], qos=1):
        """
        Inscreve em um tópico com QoS configurável
        qos=1 garante que as mensagens sejam entregues mesmo se o cliente se desconectar
        """
        self.topics.append(topic)
        self._callbacks[topic] = callback
        result = self._client.subscribe(topic, qos=qos)
        if result[0] != mqtt.MQTT_ERR_SUCCESS:
            print(f"Erro ao se inscrever no tópico {topic}: {result[0]}")
        self._client.loop_start()
        


