import json
import time
import pika
import signal
from datetime import datetime
from loguru import logger

from app.messaging.events import (
    QUEUE_USER_EVENTS,
    EVENT_USER_REGISTERED,
    EVENT_USER_UPDATED,
    EVENT_USER_DELETED
)


def process_user_registered(event: dict):
    """
    Handle user_registered event.
    In production: send real welcome email via SendGrid/AWS SES.
    """
    logger.info(
        f"[WORKER] New user registered: "
        f"{event['name']} <{event['email']}>"
    )

    logger.info(f"[WORKER] Sending welcome email to {event['email']}...")
    time.sleep(1)   
    logger.info(f"[WORKER] Welcome email sent to {event['email']} ✅")

    logger.info(f"[WORKER] Updating user count in analytics...")
    time.sleep(0.2)
    logger.info(f"[WORKER] Analytics updated ✅")


def process_user_updated(event: dict):
    logger.info(
        f"[WORKER] User {event['user_id']} updated. "
        f"Changes: {event['changes']}"
    )

    logger.info(f"[WORKER] Syncing changes to analytics service...")
    time.sleep(0.3)
    logger.info(f"[WORKER] Analytics sync complete ✅")


def process_user_deleted(event: dict):
    logger.info(
        f"[WORKER] User deleted: "
        f"{event['name']} <{event['email']}>"
    )

    logger.info(
        f"[WORKER] Sending deletion confirmation to {event['email']}..."
    )
    time.sleep(0.5)
    logger.info(f"[WORKER] Deletion email sent ✅")

    logger.info(f"[WORKER] Cleaning up user data from cache/analytics...")
    time.sleep(0.2)
    logger.info(f"[WORKER] Cleanup complete ✅")



def route_event(event: dict):
    event_type = event.get("event")

    if event_type == EVENT_USER_REGISTERED:
        process_user_registered(event)

    elif event_type == EVENT_USER_UPDATED:
        process_user_updated(event)

    elif event_type == EVENT_USER_DELETED:
        process_user_deleted(event)

    else:
        logger.warning(f"[WORKER] Unknown event type: {event_type}")



def on_message(ch, method, properties, body):
    logger.info(f"\n{'='*50}")
    logger.info(f"[WORKER] Message received at {datetime.utcnow().isoformat()}")

    try:
        event = json.loads(body.decode("utf-8"))
        logger.info(f"[WORKER] Event type: {event.get('event')}")
        logger.info(f"[WORKER] Payload: {event}")

        route_event(event)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"[WORKER] Message acknowledged ✅")

    except json.JSONDecodeError as e:
        logger.error(f"[WORKER] Invalid JSON in message: {e}")
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )

    except Exception as e:
        logger.error(f"[WORKER] Processing failed: {e}")
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True
        )



def main():
    logger.info("=" * 50)
    logger.info("User Events Worker — Starting")
    logger.info("=" * 50)

    logger.info("Connecting to RabbitMQ...")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            heartbeat=600,
            blocked_connection_timeout=300
        )
    )
    channel = connection.channel()
    logger.info("✅ Connected to RabbitMQ")

    channel.queue_declare(queue=QUEUE_USER_EVENTS, durable=True)
    logger.info(f"✅ Queue '{QUEUE_USER_EVENTS}' ready")

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_USER_EVENTS,
        on_message_callback=on_message,
        auto_ack=False
    )

    logger.info(f"Listening on queue: '{QUEUE_USER_EVENTS}'")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 50)

    def shutdown(sig, frame):
        logger.info("Shutting down worker...")
        channel.stop_consuming()

    signal.signal(signal.SIGINT, shutdown)

    channel.start_consuming()

    connection.close()
    logger.info("Worker stopped.")


if __name__ == "__main__":
    main()