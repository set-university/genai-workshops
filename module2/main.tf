provider "aws" {
  region = "us-east-1"
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" {}

####################################################
# Lambda Function (building from source)
####################################################

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.14.0"

  function_name = "bedrock-lambda-function-${random_pet.this.id}"
  description   = "AWS Lambda function to invoke Amazon Bedrock model"
  handler       = "index.handler"
  runtime       = "python3.9"
  publish       = true

  source_path = "${path.module}/src"

  # allowed_triggers = {
  #   AllowExecutionFromAPIGateway = {
  #     service    = "apigateway"
  #     source_arn = "${module.api_gateway.apigatewayv2_api_execution_arn}/*/*"
  #   }
  # }

  attach_policies = true
  policies = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]

  attach_policy_statements = true
  policy_statements = {
    invoke_bedrock_model = {
      effect = "Allow",
      actions = ["bedrock:InvokeModel"],
      resources = [
        "arn:aws:bedrock:${data.aws_region.current.name}::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
      ]
    }
  }

  tags = {
    Application = "set-genai-module2"
    Module      = "lambda_function"
  }
}

################################################################################
# PostgreSQL Serverless v2
################################################################################

data "aws_rds_engine_version" "postgresql" {
  engine  = "aurora-postgresql"
  version = "16.1"
}

resource "aws_iam_role" "vector_store_cluster_role" {
  name = "genai-cluster-role-${random_pet.this.id}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "rds.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "vector_store_cluster_role_policy" {

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "bedrock:InvokeModel",
        ]
        Effect = "Allow"
        Resource = [
          "arn:aws:bedrock:*:${data.aws_caller_identity.current.account_id}:provisioned-model/*",
          "arn:aws:bedrock:*::foundation-model/*"
        ]
      },
    ]
  })
  role = aws_iam_role.vector_store_cluster_role.id

}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.15.0"

  name = "genai-vpc-${random_pet.this.id}"
  cidr = local.vpc_cidr

  azs              = local.azs
  public_subnets   = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k)]
  private_subnets  = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 3)]
  database_subnets = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 6)]

  tags = {
    Application = "set-genai-module2"
    Module      = "vpc"
  }
}

module "aurora_postgresql_v2" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "9.10.0"

  name                 = "genai-bedrock-vector-store-${random_pet.this.id}"
  engine               = data.aws_rds_engine_version.postgresql.engine
  engine_mode          = "provisioned"
  engine_version       = data.aws_rds_engine_version.postgresql.version
  storage_encrypted    = true
  master_username      = "postgres"
  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name
  security_group_rules = {
    vpc_ingress = {
      cidr_blocks = module.vpc.private_subnets_cidr_blocks
    }
  }

  apply_immediately   = true
  skip_final_snapshot = true

  enable_http_endpoint = true

  serverlessv2_scaling_configuration = {
    min_capacity = 2
    max_capacity = 10
  }

  instance_class = "db.serverless"
  instances = {
    one = {}
  }

  iam_roles = {
    rds_cluster_role = {
      feature_name = "BEDROCK"
      role_arn     = aws_iam_role.vector_store_cluster_role.arn
    }
  }

  tags = {
    Application = "set-genai-module2"
    Module      = "rds_aurora"
  }
}

module "vector_store_bedrock_secret" {
  source = "terraform-aws-modules/secrets-manager/aws"
  version = "1.3.1"

  # Secret
  name_prefix             = "bedrock-secret-${random_pet.this.id}"
  description             = "Vector Store bedrock secret"
  recovery_window_in_days = 30
  secret_string = jsonencode({
    engine   = "postgres",
    host     = module.aurora_postgresql_v2.cluster_endpoint,
    username = "bedrock_user",
    password = "bedrock_user"
    dbname   = module.aurora_postgresql_v2.cluster_id,
    port     = 5432
  })

  tags = {
    Application = "set-genai-module2"
    Module      = "vector_store_bedrock_secret"
  }

  depends_on = [module.aurora_postgresql_v2]

}

resource "null_resource" "db_setup" {
  triggers = {
    file = filesha1("scripts/bedrock.sql")
  }
  provisioner "local-exec" {
    command = <<-EOF
			while read line; do
				echo "$line"
				aws rds-data execute-statement --resource-arn "$DB_ARN" --database  "$DB_NAME" --secret-arn "$SECRET_ARN" --sql "$line"
			done  < <(awk 'BEGIN{RS=";\n"}{gsub(/\n/,""); if(NF>0) {print $0";"}}' initial.sql)
			EOF
    environment = {
      DB_ARN     = module.aurora_postgresql_v2.cluster_arn
      DB_NAME    = module.aurora_postgresql_v2.cluster_database_name
      SECRET_ARN = module.vector_store_bedrock_secret.secret_arn
    }
    interpreter = ["bash", "-c"]
  }
  depends_on = [module.vector_store_bedrock_secret]
}

##########################
# S3 bucket for documents
##########################

module "genai_document_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.2.2"

  bucket        = "genai-bedrock-vector-store-${random_pet.this.id}"
  force_destroy = true

}

resource "aws_s3_object" "object" {
  bucket = module.genai_document_bucket.s3_bucket_id
  key    = "postgresql-16-A4.pdf"
  source = "documents/postgresql-16-A4.pdf"
  etag = filemd5("documents/postgresql-16-A4.pdf")
  depends_on = [module.genai_document_bucket]
}

####################################
# Secrets Manager
####################################

# module "vector_store_master_secret" {
#   source = "terraform-aws-modules/secrets-manager/aws"
#   version = "1.3.1"
#
#   # Secret
#   name_prefix             = "master-secret-${random_pet.this.id}"
#   description             = "Vector Store master secret"
#   recovery_window_in_days = 30
#   secret_string           = module.aurora_postgresql_v2.cluster_master_password
#
#   tags = {
#     Application = "set-genai-module2"
#     Module      = "vector_store_master_secret"
#   }
#
#   depends_on = [module.aurora_postgresql_v2]
# }



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
        Resource = ["arn:aws:bedrock:${data.aws_region.current.id}::foundation-model/amazon.titan-embed-text-v2:0"]
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
          module.aurora_postgresql_v2.cluster_arn
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

# resource "awscc_bedrock_knowledge_base" "genai-bedrock-kb" {
#   name        = "genai-bedrock-kb-${random_pet.this.id}"
#   description = "GenAI Bedrock knowledge base"
#   role_arn    = aws_iam_service_linked_role.bedrock_role.arn
#
#   storage_configuration = {
#     type = "RDS"
#     rds_configuration = {
#       credentials_secret_arn = module.vector_store_bedrock_secret.secret_arn
#       database_name          = "postgres"
#       resource_arn           = module.aurora_postgresql_v2.cluster_arn
#       table_name             = "bedrock_integration.bedrock_kb"
#       field_mapping = {
#         primary_key_field = "id"
#         text_field        = "chunks"
#         vector_field      = "embedding"
#         metadata_field    = "metadata"
#       }
#     }
#   }
#   knowledge_base_configuration = {
#     type = "VECTOR"
#     vector_knowledge_base_configuration = {
#       embedding_model_arn = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-image-generator-v2:0"
#     }
#   }
# }


###################
# HTTP API Gateway
###################

module "api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "~> 2.0"

  name          = "http-api-${random_pet.this.id}"
  description   = "HTTP API Gateway to invoke Amazon Bedrock model"
  protocol_type = "HTTP"

  create_api_domain_name = false

  cors_configuration = {
    allow_headers = [
      "content-type", "x-amz-date", "authorization", "x-api-key", "x-amz-security-token", "x-amz-user-agent"
    ]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }

  integrations = {
    "ANY /" = {
      lambda_arn             = module.lambda_function.lambda_function_arn
      payload_format_version = "2.0"
      timeout_milliseconds   = 12000
    }

    "POST /text_gen" = {
      lambda_arn             = module.lambda_function.lambda_function_arn
      payload_format_version = "2.0"
    }
  }

  tags = {
    Application = "set-genai-module2"
    Module      = "api_gateway"
  }

}
##################
# Extra resources
##################

resource "random_pet" "this" {
  length = 2
}
