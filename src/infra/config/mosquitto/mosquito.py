import paho.mqtt.client as mqtt
from typing import Callable, Dict, List
import asyncio

class MosquittoClient():
    def __init__(self, broker:str, port: int = 1883):
        self.broker = broker
        self.port = port
        self._callbacks: Dict[str, Callable[[str], None]] = {}
        self.topics: List[str] = []
        self._client = mqtt.Client()
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

    def publish(self, topic, payload):
        self._client.publish(topic, payload)
    
    def subscribe(self, topic: str, callback: Callable[[str], None]):
        self.topics.append(topic)
        self._callbacks[topic] = callback
        self._client.subscribe(topic)
        self._client.loop_start()
        


