resource "aws_lambda_function" "booking" {
  function_name = "booking_processor"
  runtime       = "python3.9"
  handler       = "booking_processor.lambda_handler"

  role = aws_iam_role.lambda_role.arn

  filename         = "booking_processor.zip"
  source_code_hash = filebase64sha256("booking_processor.zip")
}
