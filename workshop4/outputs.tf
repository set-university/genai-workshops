output "vector_store_cluster_identifier" {
  description = "Cluster Identified"
  value       = module.aurora_postgresql_v2.cluster_id
}

output "lambda_function_url" {
  description = "Lambda function URL to generate the text answer from Bedrock"
  value       = module.lambda_function.lambda_function_url
}

output "bedrock_knowledge_base" {
  description = "Bedrock knowledge base ARN"
  value       = awscc_bedrock_knowledge_base.genai-bedrock-kb.knowledge_base_arn
}