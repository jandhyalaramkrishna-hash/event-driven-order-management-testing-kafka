from flask import Flask, request, jsonify
import mysql.connector
from kafka import KafkaProducer
import json
import uuid

app = Flask(__name__)

# DB connection
conn = mysql.connector.connect(
    host="127.0.0.1",   # IMPORTANT FIX
    user="root",
    password="root123",
    database="sairam_db",
    port=3306
)



cursor = conn.cursor()

# Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

@app.route('/api/v1/order', methods=['POST'])
def create_order():
    data = request.json

    customer_id = data.get("customer_id")
    idem_key = data.get("idempotency_key")

    # 🔥 CHECK EXISTING
    cursor.execute(
        "SELECT order_id FROM idempotency_keys WHERE idempotency_key=%s",
        (idem_key,)
    )
    result = cursor.fetchone()

    if result:
        order_id = result[0]

        print(f"❌ DUPLICATE: {order_id}")

        # send to DLQ
        producer.send("dlq_topic", {
            "order_id": order_id,
            "reason": "Duplicate"
        })

        return jsonify({
            "message": "Duplicate order",
            "order_id": order_id
        })

    # ✅ CREATE NEW ORDER
    order_id = "ORD-" + str(uuid.uuid4())[:8]

    # SAVE
    cursor.execute(
        "INSERT INTO idempotency_keys (idempotency_key, order_id) VALUES (%s, %s)",
        (idem_key, order_id)
    )
    conn.commit()

    print(f"✅ NEW ORDER: {order_id}")

    # send to payment
    producer.send("payment_topic", {
        "order_id": order_id
    })

    return jsonify({
        "message": "Order created",
        "order_id": order_id
    })

if __name__ == '__main__':
    app.run(port=5000)