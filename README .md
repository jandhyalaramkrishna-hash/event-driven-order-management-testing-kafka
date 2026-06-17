SaiRam Order System - Microservices Project

---

## 📌 PROJECT OVERVIEW

This project simulates a real-world microservices system:

Order Service → Payment Service → Kitchen Service
Failures → DLQ (Dead Letter Queue) → Refund

Technologies used:

* Python (Flask)
* Kafka (Event Streaming)
* MySQL (Idempotency)
* Docker (Infra)

---

## 📦 STEP 1: START INFRA (DOCKER)

Open Terminal 1:

cd C:\sairam_project

Run:

docker-compose down -v
docker-compose up -d

Wait 15–20 seconds for Kafka & MySQL to start.

Check:

docker ps

You should see:

* kafka
* zookeeper
* mysql

---

## 🛢 STEP 2: SETUP DATABASE

Open MySQL:

docker exec -it mysql mysql -uroot -proot
mysql -u root -p

use sairam_db;

Run:

CREATE DATABASE IF NOT EXISTS sairam_db;

USE sairam_db;

CREATE TABLE IF NOT EXISTS idempotency_keys (
id INT AUTO_INCREMENT PRIMARY KEY,
idempotency_key VARCHAR(255) UNIQUE,
order_id VARCHAR(255)
);

---

## 🧹 (OPTIONAL) CLEAN DB BEFORE TEST

TRUNCATE TABLE idempotency_keys;

---

## 🚀 STEP 3: START SERVICES (VERY IMPORTANT ORDER)

Open multiple terminals:

---

## Terminal 2:

cd C:\sairam_project
python delivery_service.py

---

## Terminal 3:

cd C:\sairam_project
python payment_service.py

---

## Terminal 4:

cd C:\sairam_project
python kitchen_service.py

---

## Terminal 5:

cd C:\sairam_project
python dlq_service.py

---

## Terminal 6 (LAST):

cd C:\sairam_project\order_service
python app.py

---

## ⚠️ IMPORTANT RULE

DO NOT start app.py first
Always start it LAST

---

## 🧪 STEP 4: TEST USING POSTMAN

URL:
POST http://localhost:5000/api/v1/order

---

## ✔ NORMAL ORDER

{
"customer_id": "CUST-1001",
"idempotency_key": "order-1001"
}

---

## ✔ DUPLICATE ORDER

(Send same request again)

---

## ✔ NEW ORDER

{
"customer_id": "CUST-2001",
"idempotency_key": "order-2001"
}

---

## 🎯 EXPECTED OUTPUT

Case 1: Payment Success
→ Kitchen Service runs

Case 2: Payment Failure
→ DLQ Service
→ Refund processed

Case 3: Duplicate Order
→ DLQ Service
→ Reason: Duplicate

---

## 📊 SYSTEM FLOW

POSTMAN
↓
Order Service
↓
Kafka (payment_topic)
↓
Payment Service
↓
SUCCESS → delivery_topic → Kitchen Service
FAIL → dlq_topic → DLQ Service

---

## 🧠 KEY FEATURES

✔ Idempotency handling
✔ Retry mechanism
✔ Event-driven architecture
✔ Dead Letter Queue (DLQ)
✔ Refund handling
✔ Microservices communication via Kafka

---

## 🛑 TROUBLESHOOTING

1. Postman loading forever:
   → Delivery service not running

2. No Kafka messages:
   → Kafka not started

3. All orders duplicate:
   → Clear DB (TRUNCATE table)

4. NoBrokerAvailable:
   → Wait 15 seconds after docker start

---

## 🎉 DONE

System is now production-style simulation.
