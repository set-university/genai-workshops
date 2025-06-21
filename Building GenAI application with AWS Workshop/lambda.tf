####################################################
# Lambda Function (building from source)
####################################################

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.14.0"

  function_name              = "bedrock-lambda-function-${random_pet.this.id}"
  description                = "AWS Lambda function to invoke Amazon Bedrock model"
  handler                    = "index.handler"
  runtime                    = "python3.9"
  publish                    = true
  timeout                    = 60
  create_lambda_function_url = true

  source_path = "${path.module}/src"

  environment_variables = {
    BEDROCK_KB_ID : awscc_bedrock_knowledge_base.genai-bedrock-kb.knowledge_base_id,
    GEN_AI_MODEL_ARN : local.genai_model_arn
  }

  attach_policies = true
  policies        = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]

  attach_policy_statements = true
  policy_statements = {
    invoke_bedrock_model = {
      effect = "Allow",
      actions = [
        "bedrock:InvokeModel"
      ],
      resources = [
        local.genai_model_arn
      ]
    },
    retrieve_and_generate = {
      effect = "Allow",
      actions = [
        "bedrock:RetrieveAndGenerate",
        "bedrock:Retrieve",
      ],
      resources = [
        awscc_bedrock_knowledge_base.genai-bedrock-kb.knowledge_base_arn
      ]
    }
  }

  tags = var.aws_resource_tags

  depends_on = [awscc_bedrock_knowledge_base.genai-bedrock-kb]

}