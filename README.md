# Accounting Service

Microservice for accounting needs. Provides functionalities to Create/close accounts, fetch balances, change status.

## API Endpoints

## Features

- Send email notifications via SMTP
- Send SMS notifications via SMS gateway
- Log all notifications in database
- Support for multiple notification types
- PII masking in logs
- Correlation ID tracking
- RESTful API with OpenAPI documentation

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker & Docker Compose
- Kubernetes - minikube

## Database Schema

### notifications_log
- notification_id (PK)
- customer_id
- customer_name
- email
- phone
- notification_type
- channel (email/sms/both)
- subject
- message
- status
- transaction_id
- account_id
- amount
- correlation_id
- error_message
- sent_at
- created_at

### Health Check
```
GET /health
```

### Send Notification
```
POST /api/v1/notifications/send
```

### Get Notification by ID
```
GET /api/v1/notifications/{notification_id}
```

### Get Customer Notifications
```
GET /api/v1/notifications/customer/{customer_id}
```

### List All Notifications
```
GET /api/v1/notifications
```

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the service:
```bash
uvicorn main:app --reload --port 8004
```

### Docker Compose

```bash
docker-compose up -d
```

### Kubernetes (Minikube)

1. Build the Docker image:
```bash
docker build -t notification-service:latest .
```

2. Apply Kubernetes manifests:
```bash
kubectl apply -f k8s/
```

3. Check deployment:
```bash
kubectl get pods
kubectl get svc
```

4. Access the service:
```bash
minikube service notification-service
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SMTP_HOST`: SMTP server host
- `SMTP_PORT`: SMTP server port
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `SMS_API_KEY`: SMS gateway API key
- `SMS_API_URL`: SMS gateway API URL

## Notification Types

- `high_value_transaction`: Alert for transactions above threshold
- `account_status_change`: Account frozen/unfrozen notifications
- `transfer_success`: Successful transfer confirmation
- `transfer_failed`: Failed transfer alert
- `account_created`: New account creation confirmation
- `kyc_status_update`: KYC status change notification

## Monitoring

Logs are structured in JSON format with:
- correlationId for request tracing
- PII masking for email and phone
- Latency tracking
- Error logging

## API Documentation

Once running, access Swagger UI at:
```
http://localhost:8004/docs
```