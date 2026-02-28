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
Once the RDS instance is running, you need to initialize the tables from your EC2 instance.

1. **Download the AWS Global Bundle Certificate** (required for SSL):
   ```bash
   sudo mkdir -p /certs
   sudo wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -O /certs/global-bundle.pem
   ```

2. **Set the RDS Host and Connect**:
   ```bash
   export RDSHOST="event-booking-db.cqjac8444q7n.us-east-1.rds.amazonaws.com"

   psql "host=$RDSHOST port=5432 dbname=eventsdb user=postgres sslmode=verify-full sslrootcert=/certs/global-bundle.pem"
   ```
   *(Enter your password when prompted: `StrongPassword123`)*

3. **Run the schema script**:
   Once inside the `psql` shell:
   ```sql
   \i ../sql/schema.sql
   ```
   *(Alternatively, copy-paste the contents of `sql/schema.sql` into the terminal.)*

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
...
- **CORS Error**: Ensure `flask-cors` is installed and initialized in `app.py`.

---

## 🛠️ Useful PSQL Commands

Connect and run these to manage your data:

### Create New User
```sql
INSERT INTO users (name, email) VALUES ('Vedant', 'vedant@gmail.com');
```

### Create New Event
```sql
INSERT INTO events (title, venue, event_date, total_seats) 
VALUES ('Taylor Swift - Eras Tour', 'Wankhede Stadium, Mumbai', '2026-05-15 19:00:00', 50);
```

### Add Seats to an Event (ID 3 for example)
```sql
INSERT INTO seats (event_id, seat_number, status) VALUES 
(3, 'A1', 'AVAILABLE'), (3, 'A2', 'AVAILABLE'), (3, 'B1', 'AVAILABLE');
```

### Show All Bookings
```sql
SELECT b.id, u.name, e.title, s.seat_number, b.status 
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN events e ON b.event_id = e.id
JOIN seats s ON b.seat_id = s.id;
```

### Reset All Seats for an Event
```sql
UPDATE seats SET status = 'AVAILABLE' WHERE event_id = 3;
```
