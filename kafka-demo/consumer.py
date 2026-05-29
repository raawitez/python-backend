import json
import signal
import sys
from confluent_kafka import Consumer, KafkaException


def create_consumer(group_id: str):
    return Consumer({
        "bootstrap.servers":  "localhost:9092",
        "group.id":           group_id,
        "auto.offset.reset":  "earliest",
        "enable.auto.commit": True,
    })


def process_event(event: dict):
    event_type = event.get("event")
    user_id    = event.get("user_id")

    if event_type == "user_registered":
        print(f"    → New registration: {event.get('email')} (user_id: {user_id})")
        print(f"    → Action: Sending welcome email...")

    elif event_type == "user_updated":
        print(f"    → User {user_id} updated: {event.get('changes')}")
        print(f"    → Action: Updating analytics profile...")

    elif event_type == "user_login":
        print(f"    → User {user_id} logged in at {event.get('timestamp')}")
        print(f"    → Action: Updating last_seen timestamp...")

    elif event_type == "user_deleted":
        print(f"    → User {user_id} deleted: {event.get('email')}")
        print(f"    → Action: Sending deletion confirmation email...")

    else:
        print(f"    → Unknown event: {event_type}")


def main():
    topic    = "user-events"
    group_id = "user-service-group"

    consumer = create_consumer(group_id)
    consumer.subscribe([topic])

    print(f"[CONSUMER] Group: '{group_id}'")
    print(f"[CONSUMER] Subscribed to topic: '{topic}'")
    print(f"[CONSUMER] Waiting for messages... (Ctrl+C to stop)")
    print("-" * 60)

    running = True

    def shutdown(sig, frame):
        nonlocal running
        print("\n[CONSUMER] Shutting down...")
        running = False

    signal.signal(signal.SIGINT, shutdown)

    try:
        while running:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"[CONSUMER] ❌ Kafka error: {msg.error()}")
                continue

            print(f"\n[CONSUMER] Message received:")
            print(f"  Topic:     {msg.topic()}")
            print(f"  Partition: {msg.partition()}")
            print(f"  Offset:    {msg.offset()}")
            print(f"  Key:       {msg.key().decode('utf-8') if msg.key() else None}")

            try:
                event = json.loads(msg.value().decode("utf-8"))
                print(f"  Event:     {event.get('event')}")
                process_event(event)
                print(f"  ✅ Processed successfully")

            except json.JSONDecodeError as e:
                print(f"  ❌ Failed to parse message: {e}")

    finally:
        consumer.close()
        print("[CONSUMER] Consumer closed.")


if __name__ == "__main__":
    main()