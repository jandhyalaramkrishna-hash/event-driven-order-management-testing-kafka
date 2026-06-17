from flask import Flask, request, jsonify

from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import random

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

otp_store = {}

@app.route('/delivery/generate-otp', methods=['POST'])
def generate_otp():
    data = request.json
    order_id = data.get("order_id")

    otp = random.randint(1000, 9999)
    otp_store[order_id] = otp

    print(f"🔐 OTP for {order_id}: {otp}")

    return jsonify({"message": "OTP generated", "order_id": order_id, "otp": otp})


@app.route('/delivery/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    order_id = data.get("order_id")
    otp = data.get("otp")

    if otp_store.get(order_id) == otp:
        print(f"✅ OTP VERIFIED for {order_id}")

        producer.send("delivery_topic", {
            "order_id": order_id,
            "status": "DELIVERED"
        })

        return jsonify({"message": "Delivered successfully", "order_id": order_id})

    else:
        print(f"❌ OTP FAILED for {order_id}")
        return jsonify({"message": "Invalid OTP"}), 400


if __name__ == "__main__":
    app.run(port=5001)