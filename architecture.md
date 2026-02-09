        ┌──────────────┐
        │   Client     │
        │ (Browser /   │
        │  Postman)    │
        └──────┬───────┘
               │ HTTP
               ▼
    ┌────────────────────┐
    │  EC2 (Flask API)   │
    │  - /events         │
    │  - /book           │
    └──────┬─────────────┘
           │ Async booking
           ▼
    ┌────────────────────┐
    │   SQS Queue        │
    │  booking-queue     │
    └──────┬─────────────┘
           │ Trigger
           ▼
    ┌────────────────────┐
    │  Lambda Function   │
    │  booking_processor │
    └──────┬─────────────┘
           │ SQL
           ▼
    ┌────────────────────┐
    │  RDS PostgreSQL    │
    │  events / bookings │
    └────────────────────┘
