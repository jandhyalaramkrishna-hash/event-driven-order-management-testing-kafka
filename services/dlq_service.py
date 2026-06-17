from kafka import KafkaConsumer

import json

consumer = KafkaConsumer(
    'dlq_orders',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',   # ✅ IMPORTANT
    enable_auto_commit=True,
    group_id='dlq-group',         # ✅ ADD THIS
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🚨 DLQ Service Started...")

for msg in consumer:
    data = msg.value
    order_id = data.get("order_id")
    reason = data.get("reason")

    print(f"\n🚨 DLQ RECEIVED: {order_id}")
    print(f"❌ Reason: {reason}")
    print("💸 Refund processed successfully")