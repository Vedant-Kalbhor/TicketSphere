import json
import psycopg2
from backend.config import *

def lambda_handler(event, context):
    for record in event["Records"]:
        body = record["body"].replace("'", '"') # Basic fix for single quotes in JSON string
        data = json.loads(body)

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
            else:
                conn.rollback()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
