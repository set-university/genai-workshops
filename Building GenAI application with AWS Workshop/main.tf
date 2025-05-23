################
# Bedrock setup
################
resource "aws_iam_role" "bedrock_service_role" {
  name = "bedrock-service-role-${random_pet.this.id}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
      },
    ]
  })

  tags = var.aws_resource_tags
}

resource "aws_iam_role_policy" "bedrock_service_role_policy" {
  name = "bedrock_service_role_policy"
  role = aws_iam_role.bedrock_service_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "BedrockInvokeModelStatement"
        Action = [
          "bedrock:InvokeModel",
        ]
        Effect = "Allow"
        Resource = [local.text_embeddings_model_arn]
      },
      {
        "Sid" : "RdsDescribeStatementID",
        "Effect" : "Allow",
        "Action" : [
          "rds:DescribeDBClusters"
        ],
        "Resource" : [
          module.aurora_postgresql_v2.cluster_arn
        ]
      },
      {
        "Sid" : "DataAPIStatementID",
        "Effect" : "Allow",
        "Action" : [
          "rds-data:BatchExecuteStatement",
          "rds-data:ExecuteStatement"
        ],
        "Resource" : [
          "arn:aws:rds:${var.aws_region}:${data.aws_caller_identity.current.account_id}:cluster:*"
        ]
      },
      {
        "Sid" : "S3AccessStatement",
        "Effect" : "Allow",
        "Action" : [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        "Resource" : [
          "arn:aws:s3:::${module.genai_document_bucket.s3_bucket_id}",
          "arn:aws:s3:::${module.genai_document_bucket.s3_bucket_id}/",
          "arn:aws:s3:::${module.genai_document_bucket.s3_bucket_id}/*",
        ]
      },
      {
        "Sid" : "SecretsManagerGetStatement",
        "Effect" : "Allow",
        "Action" : [
          "secretsmanager:GetSecretValue"
        ],
        "Resource" : [
          module.vector_store_bedrock_secret.secret_arn
        ]
      }
    ]
  })
}

resource "awscc_bedrock_knowledge_base" "genai-bedrock-kb" {
  name        = "genai-bedrock-kb-${random_pet.this.id}"
  description = "GenAI Bedrock knowledge base"
  role_arn    = aws_iam_role.bedrock_service_role.arn

  storage_configuration = {
    type = "RDS"
    rds_configuration = {
      credentials_secret_arn = module.vector_store_bedrock_secret.secret_arn
      database_name          = var.bedrock_kb_db_name
      resource_arn           = module.aurora_postgresql_v2.cluster_arn
      table_name             = var.bedrock_kb_db_table_name
      field_mapping = {
        primary_key_field = "id"
        text_field        = "chunks"
        vector_field      = "embedding"
        metadata_field    = "metadata"
      }
    }
  }
  knowledge_base_configuration = {
    type = "VECTOR"
    vector_knowledge_base_configuration = {
      embedding_model_arn = local.text_embeddings_model_arn
    }
  }

  tags = var.aws_resource_tags
}

resource "awscc_bedrock_data_source" "s3_data_source" {
  name              = "genai-bedrock-data-source-${random_pet.this.id}"
  knowledge_base_id = awscc_bedrock_knowledge_base.genai-bedrock-kb.knowledge_base_id
  description       = "GenAI datasource"

  data_source_configuration = {
    s3_configuration = {
      bucket_arn = module.genai_document_bucket.s3_bucket_arn
    }
    type = "S3"
  }

  data_deletion_policy = "DELETE"

}

##################
# Extra resources
##################

resource "random_pet" "this" {
  length = 2
}
