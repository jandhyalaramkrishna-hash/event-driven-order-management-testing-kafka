from flask import Flask, request, jsonify
import mysql.connector
from kafka import KafkaProducer
import json
import uuid
import time

app = Flask(__name__)

# ===============================
# DB CONNECTION WITH RETRY (FIX)
# ===============================
conn = None

for i in range(10):
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root123",
            database="sairam_db",
            port=3306
        )
        print("✅ Connected to MySQL")
        break
    except Exception as e:
        print(f"⏳ Waiting for MySQL... Attempt {i+1}", e)
        time.sleep(5)

if conn is None:
    raise Exception("❌ Could not connect to MySQL")

cursor = conn.cursor()

# ===============================
# KAFKA CONFIG
# ===============================
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# ===============================
# CREATE ORDER API
# ===============================
@app.route('/api/v1/order', methods=['POST'])
def create_order():
    data = request.json

    customer_id = data.get("customer_id")
    idem_key = data.get("idempotency_key")

    # 🔍 CHECK DUPLICATE
    cursor.execute(
        "SELECT order_id FROM idempotency_keys WHERE idempotency_key=%s",
        (idem_key,)
    )
    result = cursor.fetchone()

    if result:
        order_id = result[0]

        print(f"❌ DUPLICATE ORDER: {order_id}")

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

    cursor.execute(
        "INSERT INTO idempotency_keys (idempotency_key, order_id) VALUES (%s, %s)",
        (idem_key, order_id)
    )
    conn.commit()

    print(f"✅ NEW ORDER: {order_id}")

    producer.send("payment_topic", {
        "order_id": order_id
    })

    return jsonify({
        "message": "Order created",
        "order_id": order_id
    })


# ===============================
# HEALTH CHECK (VERY IMPORTANT)
# ===============================
@app.route('/')
def health():
    return "API is running", 200


# ===============================
# MAIN
# ===============================
if __name__ == '__main__':
    try:
        print("🚀 Starting Order Service...")
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print("❌ ERROR IN ORDER SERVICE:", e)
        input("Press Enter to exit...")