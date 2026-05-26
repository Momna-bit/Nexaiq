"""
NexaIQ Event System — Kafka Style
Implements producer/consumer pattern exactly like Apache Kafka
"""

import json
import datetime
import threading
import queue
import time
from typing import Callable, Dict, Any

# Event Topics — like Kafka topics
TOPICS = {
    "file.uploaded": "Fired when CSV uploaded to Azure Blob",
    "pipeline.started": "Fired when pipeline begins",
    "pipeline.completed": "Fired when pipeline finishes",
    "model.trained": "Fired when AutoML completes",
    "anomaly.detected": "Fired when anomaly found",
    "alert.sent": "Fired when alert dispatched"
}

class KafkaMessage:
    """Represents a Kafka message"""
    def __init__(self, topic: str, key: str, value: Dict):
        self.topic = topic
        self.key = key
        self.value = value
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.offset = 0
        self.partition = 0

    def to_dict(self):
        return {
            "topic": self.topic,
            "key": self.key,
            "value": self.value,
            "timestamp": self.timestamp,
            "offset": self.offset,
            "partition": self.partition
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2)


class NexaIQProducer:
    """
    Kafka-style Producer
    Sends events to topics
    """
    def __init__(self, broker: str = "localhost:9092"):
        self.broker = broker
        self._message_store = {}
        self._offset_counter = {}
        print(f"[Producer] Connected to broker: {self.broker}")

    def produce(self, topic: str, key: str, value: Dict) -> KafkaMessage:
        """Send message to topic — like Kafka producer.produce()"""
        if topic not in self._message_store:
            self._message_store[topic] = []
            self._offset_counter[topic] = 0

        msg = KafkaMessage(topic=topic, key=key, value=value)
        msg.offset = self._offset_counter[topic]
        self._offset_counter[topic] += 1

        self._message_store[topic].append(msg)

        print(f"[Producer] → Topic: {topic} | Key: {key} | Offset: {msg.offset}")
        return msg

    def flush(self):
        """Flush all pending messages — like Kafka producer.flush()"""
        print("[Producer] Flushed all messages")

    def get_messages(self, topic: str) -> list:
        return self._message_store.get(topic, [])


class NexaIQConsumer:
    """
    Kafka-style Consumer
    Reads events from topics and triggers actions
    """
    def __init__(self, topics: list, group_id: str = "nexaiq-group"):
        self.topics = topics
        self.group_id = group_id
        self._handlers = {}
        self._running = False
        print(f"[Consumer] Group: {group_id} | Topics: {topics}")

    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to topic with handler function"""
        self._handlers[topic] = handler
        print(f"[Consumer] Subscribed to: {topic}")

    def process_message(self, message: KafkaMessage):
        """Process a single message"""
        handler = self._handlers.get(message.topic)
        if handler:
            print(f"[Consumer] ← Processing: {message.topic} | Key: {message.key}")
            handler(message)
        else:
            print(f"[Consumer] No handler for topic: {message.topic}")

    def consume_all(self, producer: NexaIQProducer):
        """Consume all messages from subscribed topics"""
        for topic in self.topics:
            messages = producer.get_messages(topic)
            for msg in messages:
                self.process_message(msg)


# Global event bus — shared between producer and consumer
_event_bus = {}
_event_lock = threading.Lock()

def publish_event(topic: str, key: str, data: Dict) -> KafkaMessage:
    """Publish event to the event bus"""
    with _event_lock:
        if topic not in _event_bus:
            _event_bus[topic] = []
        msg = KafkaMessage(topic=topic, key=key, value=data)
        _event_bus[topic].append(msg)
        print(f"[EventBus] Published → {topic} | {key}")
        return msg

def get_events(topic: str) -> list:
    """Get all events for a topic"""
    with _event_lock:
        return _event_bus.get(topic, [])
