from flask import Blueprint, request, jsonify
import boto3, uuid
from config import *

booking_bp = Blueprint('booking', __name__)
sqs = boto3.client("sqs", region_name=AWS_REGION)

@booking_bp.route("/book", methods=["POST"])
def book_ticket():
    data = request.json
    user_id = data["user_id"]
    event_id = data["event_id"]
    seat_ids = data["seat_ids"]  # Now expects a list

    booking_results = []

    for seat_id in seat_ids:
        booking_id = str(uuid.uuid4())
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=str({
                "booking_id": booking_id,
                "user_id": user_id,
                "event_id": event_id,
                "seat_id": seat_id
            })
        )
        booking_results.append(booking_id)

    return jsonify({
        "message": f"Successfully requested {len(seat_ids)} seats",
        "booking_ids": booking_results
    })
