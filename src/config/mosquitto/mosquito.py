import paho.mqtt.client as mqtt
from typing import Callable, Dict, List


class MosquittoClient():
    def __init__(self, broker:str, port: int = 1883):
        self.broker = broker
        self.port = port
        self._callbacks: Dict[str, Callable[[str], None]] = {}
        self.topics: List[str] = []
        self._client = mqtt.Client()
        self._client.connect(self.broker, self.port, 60)
        self._client.on_message = self._on_message
        
    def connect(self):
        if not self._client.is_connected():
            self._client.connect(self.broker, self.port, 60)
        

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if topic in self._callbacks:
            self._callbacks[topic](payload)  # Chama o callback
        else:
            print(f"⚠️ Nenhum callback registrado para o tópico {topic}")
        
    def publish(self, topic, payload):
        self._client.publish(topic, payload)
    
    def subscribe(self, topic: str, callback: Callable[[str], None]):
        self.topics.append(topic)
        self._callbacks[topic] = callback
        self._client.subscribe(topic)
        self._client.loop_start()
        

