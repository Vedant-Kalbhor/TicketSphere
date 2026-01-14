from flask import Blueprint, request, jsonify
import boto3, uuid
from config import *

booking_bp = Blueprint('booking', __name__)
sqs = boto3.client("sqs", region_name=AWS_REGION)

@booking_bp.route("/book", methods=["POST"])
def book_ticket():
    data = request.json

    booking_id = str(uuid.uuid4())

    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=str({
            "booking_id": booking_id,
            "user_id": data["user_id"],
            "event_id": data["event_id"],
            "seat_id": data["seat_id"]
        })
    )

    return jsonify({
        "message": "Booking request received",
        "booking_id": booking_id
    })
