import json
from datetime import datetime
from confluent_kafka import Producer


def delivery_report(err, msg):

    if err is not None:
        print(f"[PRODUCER] Delivery failed for message: {err}")
    else:
        print(
            f"[PRODUCER] Delivered to topic '{msg.topic()}' "
            f"partition [{msg.partition()}] "
            f"offset {msg.offset()}"
        )


def create_producer():
    return Producer({
        "bootstrap.servers": "localhost:9092",
        "acks":              "all",   
        "retries":           3,        
    })


def publish_event(producer, topic: str, key: str, event: dict):
    producer.produce(
        topic=topic,
        key=key,
        value=json.dumps(event),
        callback=delivery_report    
    )

    producer.poll(0)


def main():
    topic    = "user-events"
    producer = create_producer()

    events = [
        {
            "event":     "user_registered",
            "user_id":   1,
            "email":     "teja@gmail.com",
            "name":      "Teja Kumar",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "event":     "user_registered",
            "user_id":   2,
            "email":     "ravi@gmail.com",
            "name":      "Ravi Shankar",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "event":     "user_updated",
            "user_id":   1,
            "changes":   {"bio": "Senior developer"},
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "event":     "user_login",
            "user_id":   1,
            "email":     "teja@gmail.com",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "event":     "user_deleted",
            "user_id":   2,
            "email":     "ravi@gmail.com",
            "timestamp": datetime.utcnow().isoformat()
        },
    ]

    print(f"[PRODUCER] Publishing {len(events)} events to '{topic}'...")
    print("-" * 60)

    for event in events:
        key = str(event["user_id"])
        publish_event(producer, topic, key, event)

    print("\n[PRODUCER] Flushing — waiting for all deliveries...")
    producer.flush()
    print("[PRODUCER] All messages delivered.")


if __name__ == "__main__":
    main()