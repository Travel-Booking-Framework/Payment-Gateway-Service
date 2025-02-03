from confluent_kafka import Producer
import json
import os

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = "payment_wallet"

# Create Kafka producer instance
producer = Producer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'client.id': 'payment-gateway-producer',
})

def send_payment_notification(user_id, amount, transaction_id, status):
    """ Sends a Kafka message to notify about the payment status """
    message = {
        "user_id": user_id,
        "amount": amount,
        "transaction_id": transaction_id,
        "status": status
    }

    producer.produce(KAFKA_TOPIC, key=str(user_id), value=json.dumps(message))
    producer.flush()  # Ensure the message is delivered
