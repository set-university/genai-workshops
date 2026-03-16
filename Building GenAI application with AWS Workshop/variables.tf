variable "aws_region" {
  description = "AWS Region to deploy the infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "genai_foundational_model_id" {
  description = "GenAI Bedrock Foundational model to use"
  type        = string
  default     = "anthropic.claude-3-5-sonnet-20240620-v1:0"
}

variable "aws_resource_tags" {
  description = "A map of tags to add to AWS resources"
  type        = map(string)
  default = {
    Application = "set-genai-aws-workshop"
  }
}

variable "rds_engine" {
  description = "RDS Engine to use for the Vector database"
  type        = string
  default     = "aurora-postgresql"
}

variable "rds_engine_version" {
  description = "RDS Engine version to use for the Vector database"
  type        = string
  default     = "16.1"
}

variable "rds_master_username" {
  description = "Master username for the Vector database"
  type        = string
  default     = "postgres"
}

variable "vector_database_secret_engine" {
  description = "Vector database engine for Secrets Manager secret"
  type        = string
  default     = "postgres"
}

variable "vector_database_bedrock_kb_username" {
  description = "Vector database username for the Bedrock knowledge base"
  type        = string
  default     = "bedrock_user"
}

variable "vector_database_bedrock_kb_password" {
  description = "Vector database password for the Bedrock knowledge base"
  type        = string
  default     = "bedrock_user"
}

variable "vector_database_bedrock_port" {
  description = "Vector database port for the Bedrock knowledge base"
  type        = number
  default     = 5432
}

variable "text_embeddings_foundation_model_id" {
  description = "Bedrock Text Embeddings Foundational model to use"
  type        = string
  default     = "amazon.titan-embed-text-v2:0"
}

variable "bedrock_kb_db_name" {
  description = "Vector database name for the Bedrock knowledge base"
  type        = string
  default     = "postgres"
}

variable "bedrock_kb_db_table_name" {
  description = "Vector database table name for the Bedrock knowledge base"
  type        = string
  default     = "bedrock_integration.bedrock_kb"
}