from confluent_kafka import Producer
from django.conf import settings

def get_kafka_producer():
    producer = Producer(settings.KAFKA_PRODUCER_SETTINGS)
    return producer
