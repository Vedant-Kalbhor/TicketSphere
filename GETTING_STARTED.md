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

## 🏗️ Step 6: Data Seeding (Populate your App)
If your app is running but shows "Loading seats..." or "No events", run these commands in `psql` to populate your database:

### 1. Add a Default User
```sql
INSERT INTO users (name, email) VALUES ('User One', 'user1@example.com');
```

### 2. Add an Event (if not present)
```sql
INSERT INTO events (title, venue, event_date, total_seats) 
VALUES ('Global Tech Summit', 'Convention Center, San Jose', '2026-10-10 09:00:00', 20);
```

### 3. Generate 20 Seats for Event ID 1
```sql
-- This creates 20 seats (A1 to A20) for event 1
INSERT INTO seats (event_id, seat_number, status)
SELECT 1, 'A' || i, 'AVAILABLE' FROM generate_series(1, 20) AS i;
```

### 4. Verify everything
```sql
SELECT * FROM events;
SELECT * FROM seats LIMIT 5;
SELECT * FROM users;
```

---

## 🛠️ Maintenance: Updating Lambda (Local Windows)
Whenever you change `lambda/booking_processor.py`, run this in your **local PowerShell**:

```powershell
Compress-Archive -Path .\lambda\booking_processor.py -DestinationPath .\terraform\booking_processor.zip -Update
cd terraform
terraform apply
```

---

## 🧪 Common PSQL Queries (Reporting)

### Show All Bookings (Joined)
```sql
SELECT b.id, u.name as user, e.title as event, s.seat_number, b.status 
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN events e ON b.event_id = e.id
JOIN seats s ON b.seat_id = s.id;
```

### Check Available Seat Count
```sql
SELECT event_id, status, count(*) 
FROM seats 
GROUP BY event_id, status;
```
