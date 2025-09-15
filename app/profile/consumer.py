import pika
import json
import time

from flask_sqlalchemy import SQLAlchemy
from app import db
from ..models.User import User

def run_consumer(app):
    with app.app_context():
        url = app.config["RABBITMQ_URL"]
        exchange = app.config["RABBITMQ_EXCHANGE"]
        exchange_type = app.config["RABBITMQ_EXCHANGE_TYPE"]
        routing_key = app.config["RABBITMQ_ROUTING_KEY"]
        queue = f"{exchange}.{routing_key}"

        while True:
            try:
                conn = pika.BlockingConnection(pika.URLParameters(url))
                ch = conn.channel()

                ch.exchange_declare(exchange = exchange, exchange_type = exchange_type, durable = True)
                ch.queue_declare(queue = queue, durable = True)
                ch.queue_bind(exchange = exchange, queue = queue, routing_key = routing_key)

                def callback(_ch, method, props, body):
                    '''
                    Incoming message: {userId: uuid, firstName: "FN", lastName: "LN"}

                    '''
                    
                    try: 
                        data = json.loads(body)
                        print(" [x] Received:", data)

                        user = User(user_id = data["userId"], first_name = data["firstName"], last_name = data["lastName"])

                        db.session.add(user)
                        db.session.commit()
                        ch.basic_ack(delivery_tag=method.delivery_tag)

                        print(" [x] Successfully consumed message")

                    except Exception as e:
                        db.session.rollback()
                        print("Database Error:", e)


                ch.basic_consume(queue, on_message_callback = callback, auto_ack = False)
                
                try:
                    message = (
                        "Consumer started successfully.\n"
                        f"- Bound to exchange: '{exchange}'\n"
                        f"- Using routing key: '{routing_key}'\n"
                        f"- Listening on queue: '{queue}'\n"
                        " [x] To exit press CTRL+C"
                    )
                    print(message)
                    ch.start_consuming()
                except KeyboardInterrupt:
                    print("Shutting down consumer...")
                    ch.stop_consuming()
                    conn.close()
                    break

            except Exception as e:
                print("Consumer Error:", e, "— retrying in 5s")
                time.sleep(5)