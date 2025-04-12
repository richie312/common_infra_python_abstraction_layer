import requests
import redis
import json
from flask import Flask, request, jsonify
from kafka_producer import produce_message, create_topic, consume_messages
from confluent_kafka import Consumer, KafkaException, KafkaError


app = Flask(__name__)
cache_map = {}

def produce(topic,key,msg):
    
    if not topic or not msg:
        return jsonify({'error': 'Topic and value are required'}), 400

    produce_message(topic, key, msg)
    return jsonify({'status': 'Message produced'}), 200

@app.route('/inject_retirement_params', methods=['POST'])
def inject_retirement_params():
    topic = "test-topic"
    key = "my-key"
    incoming_data = json.loads(request.data.decode('utf-8'))
    # TODO will replace this with redis service
    if str(incoming_data) in list(cache_map.keys()):
        value = cache_map[str(incoming_data)]
        cache_hit = True
    else:
        value = requests.get("http://localhost:8000/default-values/")
        cache_map[str(incoming_data)] = value
        api_hit = True
    
    try:
        value.status_code == 200
        value = value.text
    except AttributeError:
        return jsonify({'error': 'Failed to fetch default value'}), 500
    
    if not topic or not value:
        return jsonify({'error': 'Topic and value are required'}), 400
    
    # Produce the message to Kafka
    produce(topic, key, value)
    return jsonify({'status': 'Message produced_{}'.format(value)}), 200

@app.route('/consume', methods=['GET'])
def consume():
    topic = request.args.get('topic', 'test-topic')  # Default to 'test-topic' if no topic is provided
    try:
        consume_messages(topic)
        return jsonify({'status': f'Consuming messages from topic: {topic}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5001)