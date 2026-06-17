# 🚀 Event-Driven Order Management Testing (Kafka)

## 📌 Project Overview

This project demonstrates **end-to-end testing of a Kafka-based Event-Driven Microservices Architecture** for an Order Management System.

It simulates real-world enterprise workflow including order processing, payment, kitchen preparation, delivery, and failure handling using DLQ.

---

## 🏗️ Architecture Flow

Client → Order Service (API)
          ↓
      Kafka Topic
          ↓
    Payment Service
          ↓ 
   Kitchen Service
          ↓
  Delivery Service
          ↓
   Order Completed 
          ↓
❌ Failed Events → DLQ Service
```
## ⚙️ Tech Stack

* Python (FastAPI)
* Apache Kafka
* Zookeeper
* Docker & Docker Compose
* Postman / Newman
* JSON Validation

---

## 🧪 Testing Coverage

* API Testing (POST /orders)
* Kafka Event Validation
* Idempotency Testing (Duplicate Order Handling)
* Dead Letter Queue (DLQ) Testing
* End-to-End Workflow Testing
* Microservices Integration Testing

---

## 🚀 How to Run

### 1️⃣ Start Infrastructure

```
docker-compose up -d
```

### 2️⃣ Start Services (Open multiple terminals)

```
python services/payment_service.py
python services/kitchen_service.py
python services/dlq_service.py
python services/delivery_service.py
```

### 3️⃣ Start API

```
python order_service/app.py
```

---

## 📬 Postman Collection

Available inside:

```
postman/
```

---

## ✅ Key Highlights

* Event-driven architecture testing using Kafka
* End-to-End microservices workflow validation
* Kafka producer-consumer verification
* Idempotency validation for duplicate requests
* DLQ testing for failure handling
* Real-time order lifecycle simulation

---

## 📊 Sample Output

* Successful Order Processing
* Duplicate Order Blocked (409 Conflict)
* Failed Event Routed to DLQ

---

## 🎯 Why This Project Matters

This project demonstrates **enterprise-level QA capabilities** including:

* Distributed system testing
* Event-driven validation
* API + Messaging integration
* Failure scenario handling

---

## 👨‍💻 Author

Ramakrishna Jandhyala
Email: [jandhyalaramkrishna@gmail.com](mailto:jandhyalaramkrishna@gmail.com)
