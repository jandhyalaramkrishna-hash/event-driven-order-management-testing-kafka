from kafka import KafkaConsumer
import json
import time

consumer = KafkaConsumer(
    'delivery_topic',   # 🔥 ONLY after payment success
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='kitchen-group'
)

print("👨‍🍳 Kitchen Service Started...")

for msg in consumer:
    order_id = msg.value["order_id"]

    print(f"\n👨‍🍳 Preparing {order_id}")
    time.sleep(2)

    print(f"🍽️ Order READY {order_id}")