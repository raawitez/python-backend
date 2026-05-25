# consumer.py

import pika
import json
import time


def process_event(event: dict):
    """
    Handle a user event.
    Each event type gets different processing logic.
    """
    event_type = event.get("event")

    if event_type == "user_registered":
        print(
            f"  [PROCESSING] New user registered: "
            f"{event.get('email')} (id: {event.get('user_id')})"
        )
        print(f"  [PROCESSING] Sending welcome email...")
        time.sleep(0.5)   # simulate email sending
        print(f"  [PROCESSING] Welcome email sent.")

    elif event_type == "user_updated":
        print(
            f"  [PROCESSING] User {event.get('user_id')} updated: "
            f"{event.get('changes')}"
        )

    elif event_type == "user_deleted":
        print(
            f"  [PROCESSING] User deleted: "
            f"{event.get('email')} (id: {event.get('user_id')})"
        )
        print(f"  [PROCESSING] Sending deletion confirmation email...")
        time.sleep(0.3)
        print(f"  [PROCESSING] Deletion email sent.")

    elif event_type == "user_login":
        print(
            f"  [PROCESSING] User login: "
            f"{event.get('email')} at {event.get('timestamp')}"
        )

    else:
        print(f"  [PROCESSING] Unknown event type: {event_type}")


def callback(ch, method, properties, body):
    """
    Called automatically by pika for every message.

    ch         = channel
    method     = has delivery_tag for acknowledgement
    properties = message metadata
    body       = message content (bytes)
    """
    print(f"\n[CONSUMER] Message received:")

    try:
        # Decode bytes to string, then parse JSON to dict
        message = json.loads(body.decode("utf-8"))
        print(f"  Event: {message.get('event')}")
        print(f"  Data:  {message}")

        # Process the event
        process_event(message)

        # Send acknowledgement — tells RabbitMQ to remove message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"  [ACK] Message acknowledged and removed from queue.")

    except Exception as e:
        print(f"  [ERROR] Failed to process message: {e}")
        # Negative acknowledgement — requeue the message
        # nack = "I failed, please try again"
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True    # put it back in queue for retry
        )


def main():
    queue_name = "user_events"

    print(f"[CONSUMER] Connecting to RabbitMQ...")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            heartbeat=600
        )
    )
    channel = connection.channel()

    # Declare same queue as producer
    # Safe to call even if queue already exists
    channel.queue_declare(queue=queue_name, durable=True)

    # Only fetch 1 message at a time
    # Don't send next until current is acknowledged
    channel.basic_qos(prefetch_count=1)

    # Register callback — called for each message
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False    # manual ack — we control when message is removed
    )

    print(f"[CONSUMER] Waiting for messages in '{queue_name}'...")
    print(f"[CONSUMER] Press Ctrl+C to stop.")
    print("-" * 50)

    try:
        # Blocks here forever — processes messages as they arrive
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[CONSUMER] Stopping...")
        channel.stop_consuming()

    connection.close()
    print("[CONSUMER] Connection closed.")


if __name__ == "__main__":
    main()