@echo off

echo ===============================
echo CLEANING DOCKER ENVIRONMENT
echo ===============================

docker-compose down -v
docker system prune -f

echo ===============================
echo FREEING PORT 3306 (MySQL)
echo ===============================

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3306') do taskkill /PID %%a /F

echo ===============================
echo STARTING DOCKER SERVICES
echo ===============================

docker-compose up -d

echo Waiting for Kafka & MySQL...
timeout /t 15

echo ===============================
echo STARTING MICROSERVICES
echo ===============================

start cmd /k "cd order_service && python app.py"
start cmd /k "cd .. && python delivery_service.py"
start cmd /k "cd .. && python payment_service.py"
start cmd /k "cd .. && python kitchen_service.py"

echo ===============================
echo ALL SERVICES STARTED
echo ===============================

pause