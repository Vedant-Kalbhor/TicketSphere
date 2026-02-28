# 🚀 TicketSphere — Project Starting Guide

This guide provides a step-by-step walkthrough to get the **TicketSphere** platform up and running from scratch.

---

## 📋 Prerequisites
- **AWS Account** with CLI configured (`aws configure`).
- **Terraform** installed.
- **Python 3.x** installed.
- **PostgreSQL Client** (`psql`) installed (optional, for DB setup).

---

## 🛠️ Step 1: Provision Infrastructure (Terraform)
First, we need to create the AWS resources (SQS, Lambda, IAM Roles, etc.).

1. Navigate to the terraform directory:
   ```bash
   cd terraform
   ```
2. Initialize and apply:
   ```bash
   terraform init
   terraform apply
   ```
3. **Note the Outputs**: After completion, Terraform will provide details like the **SQS Queue URL**. You will also need the **RDS Endpoint** and **EC2 Public IP** from your AWS Console.

---

## 🗄️ Step 2: Database Setup (RDS)
Once the RDS instance is running, you need to initialize the tables.

1. Connect to your RDS instance:
   ```bash
   psql -h <RDS_ENDPOINT> -U postgres -d eventsdb
   ```
2. Run the schema script:
   ```sql
   \i ../sql/schema.sql
   ```
   *(Alternatively, copy-paste the contents of `sql/schema.sql` into your database tool.)*

---

## 🐍 Step 3: Start the Backend (EC2)
The backend acts as the bridge between the user and the async booking system.

1. **SSH into your EC2 instance**:
   ```bash
   ssh -i "mywebserver-key.pem" ec2-user@<EC2_PUBLIC_IP>
   ```
2. **Deploy Code**: Copy the `backend/` folder to the EC2 instance.
3. **Configure**: Update `backend/config.py` with your live AWS credentials and endpoints:
   - `DB_HOST`: Your RDS Endpoint.
   - `SQS_QUEUE_URL`: Your SQS URL from Step 1.
4. **Run the App**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python3 app.py
   ```
   *The backend will now be listening on port `5000`.*

---

## 🌐 Step 4: Run the Frontend
The frontend is a lightweight vanilla app that runs in your browser.

1. **Configure API URL**: Open `frontend/app.js` and update `API_BASE_URL`:
   ```javascript
   const API_BASE_URL = "http://<EC2_PUBLIC_IP>:5000";
   ```
2. **Open the App**: Simply open `frontend/index.html` in any modern web browser.

---

## 🔍 Where to find credentials/IPs?

| What | Where to find it |
| --- | --- |
| **EC2 Public IP** | AWS Console > EC2 Instances > [Select your instance] > Details |
| **RDS Endpoint** | AWS Console > RDS > Databases > [Select your DB] > Connectivity & security |
| **SQS Queue URL** | Terraform output OR AWS Console > SQS > Queues |
| **DB Password** | Set in `backend/config.py` (Default: `StrongPassword123`) |

---

## 🛑 Common Troubleshooting
- **Connection Timeout**: Ensure your EC2 Security Group allows inbound traffic on port `5000` and `22`.
- **RDS Access**: Ensure the RDS Security Group allows inbound traffic from your EC2 instance's IP on port `5432`.
- **CORS Error**: Ensure `flask-cors` is installed and initialized in `app.py`.
