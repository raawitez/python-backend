import pika
import json
import time


def process_event(event: dict):
    event_type = event.get("event")

    if event_type == "user_registered":
        print(
            f"  [PROCESSING] New user registered: "
            f"{event.get('email')} (id: {event.get('user_id')})"
        )
        print(f"  [PROCESSING] Sending welcome email...")
        time.sleep(0.5)   
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
        message = json.loads(body.decode("utf-8"))
        print(f"  Event: {message.get('event')}")
        print(f"  Data:  {message}")

        process_event(message)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"  [ACK] Message acknowledged and removed from queue.")

    except Exception as e:
        print(f"  [ERROR] Failed to process message: {e}")
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True   
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

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False    
    )

    print(f"[CONSUMER] Waiting for messages in '{queue_name}'...")
    print(f"[CONSUMER] Press Ctrl+C to stop.")
    print("-" * 50)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[CONSUMER] Stopping...")
        channel.stop_consuming()

    connection.close()
    print("[CONSUMER] Connection closed.")


if __name__ == "__main__":
    main()