import boto3

ses = boto3.client("ses")

def lambda_handler(event, context):
    ses.send_email(
        Source="noreply@events.com",
        Destination={"ToAddresses": ["user@email.com"]},
        Message={
            "Subject": {"Data": "Booking Confirmed"},
            "Body": {"Text": {"Data": "Your ticket is confirmed"}}
        }
    )
