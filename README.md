# 🎟️ TicketSphere — Cloud-Native Event Booking Platform

A **BookMyShow-like cloud-native event booking system** built on AWS to demonstrate **scalable backend design, async processing, and infrastructure as code**.

---

## 🚀 Features

- Browse events (concerts, conferences, workshops)
- Book tickets with async processing
- High-concurrency safe booking flow
- Decoupled architecture using SQS
- Serverless booking processor (Lambda)
- Secure IAM-based access (no hardcoded secrets)
- Fully reproducible infrastructure using Terraform

---

## 🧠 System Design Highlights

- **Async booking via SQS** to prevent race conditions
- **EC2 backend** focuses only on request validation
- **Lambda consumers** handle booking finalization
- **RDS (PostgreSQL)** ensures transactional consistency
- **IAM Roles** used everywhere instead of access keys


## 🏗️ Architecture Overview

Frontend → EC2 (Flask API) → SQS → Lambda → RDS  
All components live inside a **custom VPC** with controlled access.

---

## 🧰 Tech Stack

### Backend
- Python (Flask)
- Boto3
- Psycopg2

### AWS
- EC2 (API server)
- RDS (PostgreSQL)
- SQS (booking queue)
- Lambda (booking processor)
- IAM (role-based access)
- VPC, Subnets, Security Groups

### Infrastructure as Code
- Terraform

---

## 🔐 Security Best Practices

- No AWS access keys in code
- EC2 & Lambda use IAM Roles
- RDS in private subnets
- Principle of least privilege

---

## 🧪 API Endpoints

### Get Events
```
GET /events
```

### Book Ticket
```
POST /book
```

## ⚙️ Local / EC2 Setup

```bash
pip install -r requirements.txt
python3 app.py
```

Backend runs on:

```
http://<EC2_PUBLIC_IP>:5000
```

---

## 📦 Terraform Deployment

```bash
terraform init
terraform apply
```

Creates:

* SQS queue
* Lambda function
* IAM roles & policies

---

## 🧑‍💻 Author

**Vedant Kalbhor**

---
⭐ If this project helped you learn something - star the repo!
