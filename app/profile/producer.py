import pika
import json
import os

from flask import current_app

def publish_profile_creation_failed(payload, ch):
    """Publishes a message indicating that profile creation failed."""
    try:
        # url = current_app.config["RABBITMQ_URL"]

        exchange = current_app.config["RABBITMQ_FAILURE_EXCHANGE"]
        exchange_type = current_app.config["RABBITMQ_FAILURE_EXCHANGE_TYPE"]
        routing_key = current_app.config["RABBITMQ_FAILURE_ROUTING_KEY"]

        # conn = pika.BlockingConnection(pika.URLParameters(url))
        # ch = conn.channel()

        ch.exchange_declare(
            exchange = exchange, 
            exchange_type = exchange_type, 
            durable = True
        )
        
        message = json.dumps(payload)

        ch.basic_publish(
            exchange = exchange,
            routing_key = routing_key,
            body = message
        )
        print(f" [x] Published failure event: {message}")

        # conn.close()

    except Exception as e:
        print(f" [x] Error publishing failure event: {e}")