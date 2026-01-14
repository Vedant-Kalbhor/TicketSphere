import json
import psycopg2
from backend.config import *

def lambda_handler(event, context):
    for record in event["Records"]:
        body = eval(record["body"])

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
                (body["seat_id"],)
            )
            status = cur.fetchone()[0]

            if status == "AVAILABLE":
                cur.execute(
                    "UPDATE seats SET status='BOOKED' WHERE id=%s",
                    (body["seat_id"],)
                )

                cur.execute(
                    "INSERT INTO bookings VALUES (%s,%s,%s,%s,'CONFIRMED',NOW())",
                    (
                        body["booking_id"],
                        body["user_id"],
                        body["event_id"],
                        body["seat_id"]
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
