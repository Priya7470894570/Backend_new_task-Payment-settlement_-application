# Consumer for Payment Events
from confluent_kafka import Consumer, KafkaError

# Define the Kafka consumer configuration
payment_consumer_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'payment_consumer_group',   # Unique group ID for payment events
    'auto.offset.reset': 'earliest'        # Start consuming from the beginning of the topic
}

# Create a Kafka consumer instance
payment_consumer = Consumer(payment_consumer_config)

# Subscribe to the payment topic
payment_consumer.subscribe(['payment_topic'])

# Start consuming messages
while True:
    msg = payment_consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print(f"Reached end of partition {msg.partition()}")
        else:
            print(f"Error while consuming: {msg.error()}")
    else:

        # Process the payment event
        print(f"Received message: {msg.value()}")