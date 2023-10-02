# Consumer for Settlement Events
from confluent_kafka import Consumer, KafkaError

# Define the Kafka consumer configuration
settlement_consumer_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'settlement_consumer_group', # Unique group ID for settlement events
    'auto.offset.reset': 'earliest'         # Start consuming from the beginning of the topic
}

# Create a Kafka consumer instance
settlement_consumer = Consumer(settlement_consumer_config)

# Subscribe to the settlement topic
settlement_consumer.subscribe(['settlements_topic'])

# Start consuming messages
while True:
    msg = settlement_consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print(f"Reached end of partition {msg.partition()}")
        else:
            print(f"Error while consuming: {msg.error()}")
    else:
        # Process the settlement event
        print(f"Received message: {msg.value()}")
