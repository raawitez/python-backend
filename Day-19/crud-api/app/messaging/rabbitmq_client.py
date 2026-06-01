import json
import pika
from loguru import logger

class RabbitMQPublisher:
    def __init__(self, host: str = "localhost", port: int = 5672):
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            self.channel = self.connection.channel()
            logger.info("RabbitMQ publisher connected")

        except Exception as e:
            logger.error(f"RabbitMQ connection failed: {e}")
            self.connection = None
            self.channel = None

    def disconnect(self):
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("RabbitMQ publisher disconnected")
        except Exception as e:
            logger.warning(f"Error closing RabbitMQ connection: {e}")
        
    def declare_queue(self, queue_name: str):
        if self.channel:
            self.channel.queue_declare(
                queue=queue_name,
                durable=True
            )
        
    def publish(self, queue_name: str, event: dict)->bool:
        if not self.channel:
            logger.warning(
                f"RabbitMQ unavailable - skipping event: "
                f"{event.get('event')} for queue '{queue_name}'"
            )
            return False
            
        try:
            self.declare_queue(queue_name)

            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(event),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json"
                )
            )
            logger.info(
                f"[RABBITMQ] Published '{event.get('event')}'"
                f"to queue '{queue_name}'"
            )
            return True
            
        except Exception as e:
            logger.error(f"[RABBITMQ] Publish failed: {e}")
            self.connect()
            return False

publisher = RabbitMQPublisher()