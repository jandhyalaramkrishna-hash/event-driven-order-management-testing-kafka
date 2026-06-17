from kafka import KafkaConsumer, KafkaProducer
import json
import random
import time

# Kafka Consumer
consumer = KafkaConsumer(
    'payment_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='payment-group'
)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("💰 Payment Service Started...")

# Listen to messages
for message in consumer:
    data = message.value
    order_id = data.get("order_id")

    print(f"\n💰 Processing {order_id}")

    success = False

    # Retry logic (3 attempts)
    for i in range(1, 4):
        print(f"🔁 Attempt {i}")
        time.sleep(1)

        # 30% success chance
        if random.random() < 0.3:
            success = True
            print(f"✅ Payment SUCCESS for {order_id}")
            break
        else:
            print(f"❌ Payment FAILED attempt {i}")

    # Final decision
    if success:
        producer.send("delivery_topic", {
            "order_id": order_id,
            "status": "SUCCESS"
        })
    else:
        print(f"🚨 Payment FAILED → DLQ {order_id}")

        producer.send("dlq_topic", {
            "order_id": order_id,
            "reason": "Payment Failed"
        })