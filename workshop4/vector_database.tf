################################################################################
# PostgreSQL Serverless v2
################################################################################

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
  tags = var.aws_resource_tags
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

  tags = var.aws_resource_tags
}

module "aurora_postgresql_v2" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "9.10.0"

  name                 = "genai-bedrock-vector-store-${random_pet.this.id}"
  engine               = var.rds_engine
  engine_mode          = "provisioned"
  engine_version       = var.rds_engine_version
  storage_encrypted    = true
  master_username      = var.rds_master_username
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
      feature_name = "SageMaker"
      role_arn     = aws_iam_role.vector_store_cluster_role.arn
    }
  }

  tags = var.aws_resource_tags
}

module "vector_store_bedrock_secret" {
  source = "terraform-aws-modules/secrets-manager/aws"
  version = "1.3.1"

  # Secret
  name_prefix             = "bedrock-secret-${random_pet.this.id}"
  description             = "Vector Store bedrock secret"
  recovery_window_in_days = 30
  secret_string = jsonencode({
    engine              = var.vector_database_secret_engine,
    host                = module.aurora_postgresql_v2.cluster_endpoint,
    username            = var.vector_database_bedrock_kb_username,
    password            = var.vector_database_bedrock_kb_password
    dbClusterIdentifier = module.aurora_postgresql_v2.cluster_id,
    port                = var.vector_database_bedrock_port
  })

  tags = var.aws_resource_tags

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
				aws rds-data execute-statement --region "$REGION" --resource-arn "$DB_ARN" --database  "$DB_NAME" --secret-arn "$SECRET_ARN" --sql "$line"
			done  < <(awk 'BEGIN{RS=";\n"}{gsub(/\n/,""); if(NF>0) {print $0";"}}' scripts/bedrock.sql)
			EOF
    environment = {
      DB_ARN     = module.aurora_postgresql_v2.cluster_arn
      DB_NAME    = module.aurora_postgresql_v2.cluster_database_name
      SECRET_ARN = module.aurora_postgresql_v2.cluster_master_user_secret[0].secret_arn
      REGION     = data.aws_region.current.id
    }
    interpreter = ["bash", "-c"]
  }
  depends_on = [module.aurora_postgresql_v2]
}