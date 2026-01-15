resource "aws_sqs_queue" "booking_queue" {
  name                       = "booking-queue"
  visibility_timeout_seconds = 60
  max_message_size           = 262144
}
