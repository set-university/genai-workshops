output "lambda_function_url" {
  description = "Lambda function URL to generate the text answer from Bedrock"
  value       = module.lambda_function.lambda_function_url
}