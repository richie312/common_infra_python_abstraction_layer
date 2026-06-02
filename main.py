import os
import subprocess
import json
import datetime
import redis
from flask import Flask, request, jsonify
from kafka_flask_server.kafka_producer import produce_message, consume_messages, create_topic
from confluent_kafka import Consumer, KafkaException, KafkaError


app = Flask(__name__)

# Instantiate Redis client
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)



# -------------------------
# Config
# -------------------------
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")

BACKUP_DIR = os.getenv("MYSQL_BACKUP_DIR", "/dumps")

os.makedirs(BACKUP_DIR, exist_ok=True)

# -------------------------
# OPS: MySQL Dump
# -------------------------
@app.route("/ops/mysql/dump", methods=["POST"])
def mysql_dump():

    if not MYSQL_PASSWORD:
        return jsonify({"error": "MYSQL_ROOT_PASSWORD not set"}), 500

    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"mysql_dump_{ts}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)

    cmd = [
        "mysqldump",
        "-h", MYSQL_HOST,
        "-u", MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        "--single-transaction",
        "--routines",
        "--events",
        "--all-databases"
    ]

    try:
        with open(filepath, "w") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)

        return jsonify({
            "status": "dump_created",
            "file": filepath
        }), 200

    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "dump_failed",
            "error": e.stderr.decode()
        }), 500
    
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
    app.run(host = '0.0.0.0',debug=True,port=5003)