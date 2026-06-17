import time
from kafka import KafkaConsumer
import json

print("DLQ Service Starting...")

consumer = None

# ===============================
# RETRY FOR KAFKA CONNECTION
# ===============================
for i in range(10):
    try:
        consumer = KafkaConsumer(
            'dlq_topic',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id='dlq-group',
            auto_offset_reset='earliest'
        )
        print("Connected to Kafka (DLQ)")
        break
    except Exception as e:
        print(f"Waiting for Kafka... Attempt {i+1}", e)
        time.sleep(5)

if consumer is None:
    raise Exception("Could not connect to Kafka")

print("DLQ Service Started...")

# ===============================
# CONSUME MESSAGES
# ===============================
for message in consumer:
    data = message.value

    print("DLQ EVENT RECEIVED:")
    print(data)

    # Here you can log/store failures
    # Example:
    # write to file / DB / monitoring