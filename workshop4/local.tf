locals {
  vpc_cidr                     = "10.0.0.0/16"
  azs                          = slice(data.aws_availability_zones.available.names, 0, 3)
  genai_model_arn = "arn:aws:bedrock:${var.aws_region}::foundation-model/${var.genai_foundational_model_id}"
  text_embeddings_model_arn = "arn:aws:bedrock:${var.aws_region}::foundation-model/${var.text_embeddings_foundation_model_id}"
}