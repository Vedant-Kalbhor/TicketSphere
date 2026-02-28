import json
import psycopg2
import os

# Hardcoded for Lambda stability (matches your config.py)
DB_HOST = "event-booking-db.cqjac8444q7n.us-east-1.rds.amazonaws.com"
DB_NAME = "eventsdb"
DB_USER = "postgres"
DB_PASSWORD = "StrongPassword123"

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    
    for record in event["Records"]:
        try:
            # Clean single quotes if they exist in the SQS body
            body_str = record["body"].replace("'", '"')
            data = json.loads(body_str)
            print(f"Processing booking: {data}")

            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()

            try:
                cur.execute("BEGIN")

                cur.execute(
                    "SELECT status FROM seats WHERE id=%s FOR UPDATE",
                    (data["seat_id"],)
                )
                status = cur.fetchone()[0]

                if status == "AVAILABLE":
                    cur.execute(
                        "UPDATE seats SET status='BOOKED' WHERE id=%s",
                        (data["seat_id"],)
                    )

                    cur.execute(
                        "INSERT INTO bookings (id, user_id, event_id, seat_id, status, created_at) VALUES (%s,%s,%s,%s,'CONFIRMED',NOW())",
                        (
                            data["booking_id"],
                            data["user_id"],
                            data["event_id"],
                            data["seat_id"]
                        )
                    )
                    conn.commit()
                    print(f"Successfully booked seat {data['seat_id']}")
                else:
                    conn.rollback()
                    print(f"Seat {data['seat_id']} already occupied.")

            except Exception as e:
                conn.rollback()
                print(f"Database error: {str(e)}")
                raise e
            finally:
                conn.close()

        except Exception as e:
            print(f"Error processing record: {str(e)}")
            continue
