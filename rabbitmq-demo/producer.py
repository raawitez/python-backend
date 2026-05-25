import pika
import json
from datetime import datetime

def get_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            heartbeat=600
        )
    )
    return connection

def publish_message(queue_name: str, message:dict):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    message_body = json.dumps(message)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message_body,
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json"
        )
    )
    print(f"[PRODUCER] Sent message to '{queue_name}': {message}")
    connection.close()

def main():
    queue_name = "user_events"
    events = [
        {
            "event": "user_registered",
            "user_id": 1,
            "email": "teja@gmail.com",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "event": "user_registered",
            "user_id": 1,
            "email": "ravi@gmail.com",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "event": "user_updated",
            "user_id": 1,
            "changes": {"bio": "Updated bio"},
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "event":     "user_deleted",
            "user_id":   3,
            "email":     "priya@gmail.com",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "event":     "user_login",
            "user_id":   1,
            "email":     "teja@gmail.com",
            "timestamp": datetime.utcnow().isoformat()
        }
    ]

    print(f"[PRODUCER] Publishing {len(events)} events to '{queue_name}'...")
    print("-"*50)

    for event in events:
        publish_message(queue_name, event)
    
    print("-"*50)
    print(f"[PRODUCER] Done. All {len(events)} messages sent.")

if __name__ == "__main__":
    main()