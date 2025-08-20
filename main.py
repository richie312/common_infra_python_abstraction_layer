import json
import redis
from flask import Flask, request, jsonify
from kafka_flask_server.kafka_producer import produce_message, consume_messages, create_topic
from confluent_kafka import Consumer, KafkaException, KafkaError


app = Flask(__name__)

# Instantiate Redis client
redis_client = redis.StrictRedis(host='redis-server', port=6379, db=0, decode_responses=True)


def produce(topic,key,msg):
    if not topic or not msg:
        return jsonify({'error': 'Topic and value are required'}), 400
    # create topic if not exist
    create_topic(topic)
    # produce topic
    produce_message(topic, key, msg)
    return jsonify({'status': 'Message produced'}), 200


@app.route('/produce', methods=['POST'])
def produce_data():
    incoming_data = json.loads(request.data.decode('utf-8'))
    topic = incoming_data.get('topic')
    key = incoming_data.get('key')
    value = incoming_data.get('value')
    # Produce the message to Kafka
    produce(topic, key, value)
    return jsonify({'status': 'Message produced_{}'.format(value)}), 200

@app.route('/consume', methods=['GET'])
def consume():
    topic = request.args.get('topic', 'test-topic')  # Default to 'test-topic' if no topic is provided
    try:
        msg = consume_messages(topic)
        # Save the message to Redis
        if msg is not None:
            redis_client.rpush('messages', msg)
        
        # Retrieve all messages from Redis
        all_messages = redis_client.lrange('messages', 0, -1)
        collection = {"data": all_messages}
        #TODO set expiration to delete messages from redis
        return jsonify(collection), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5000)