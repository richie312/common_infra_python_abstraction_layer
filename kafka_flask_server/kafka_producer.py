from confluent_kafka import Producer
import os
import sys
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer, KafkaException, KafkaError

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


def create_producer():
    conf = {
        'bootstrap.servers': 'common_infra:9092',  # Replace with your Kafka broker(s)
        'client.id': 'flask-producer',
        'security.protocol': 'PLAINTEXT'
    }
    return Producer(**conf)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_message(topic, key, value):
    producer = create_producer()
    producer.produce(topic, key=key, value=value, callback=delivery_report)
    producer.flush()

def create_topic(topic_name, num_partitions=3, replication_factor=1):
    """
    Creates a Kafka topic using the confluent-kafka AdminClient.

    :param broker: Kafka broker address (e.g., 'localhost:9092')
    :param topic_name: Name of the topic to create
    :param num_partitions: Number of partitions for the topic
    :param replication_factor: Replication factor for the topic
    """
    admin_client = AdminClient({'bootstrap.servers': 'common_infra:9092'})

    # Define the topic configuration
    topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

    try:
        # Create the topic
        futures = admin_client.create_topics([topic])

        # Wait for the operation to complete
        for topic, future in futures.items():
            try:
                future.result()  # Wait for the topic to be created
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic '{topic}': {e}")
    except Exception as e:
        print(f"Error creating topic: {e}")

def create_consumer():
    # Configuration for the Kafka consumer
    conf = {
        'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker(s)
        'group.id': 'my-consumer-group',        # Consumer group ID
        'auto.offset.reset': 'earliest',        # Start reading at the earliest message
    }
    return Consumer(**conf)

def consume_messages(topic):
    """
    Consumes messages from the specified Kafka topic.
    """
    # Create a Kafka consumer
    consumer = create_consumer()
    consumer.subscribe([topic])  # Subscribe to the topic

    try:
        print(f"Consuming messages from topic: {topic}")
        retries = 0  # Initialize retry counter
        max_retries = 3  # Set maximum retries
        while retries < max_retries:
            msg = consumer.poll(1.0)  # Poll for messages (timeout in seconds)
            if msg is None:
                retries += 1
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f"Reached end of partition: {msg.topic()} [{msg.partition()}]")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Successfully received a message
                
                message = msg.value().decode('utf-8')
                return message
    except KeyboardInterrupt:
        print("Consumer interrupted by user")
    finally:
        # Close the consumer to commit final offsets
        consumer.close()