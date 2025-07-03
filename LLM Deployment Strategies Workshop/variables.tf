variable "aws_region" {
  type        = string
  description = "AWS region to deploy the infrastructure"
  default     = "us-east-1"
}

variable "aws_ec2_instance_type" {
  type        = string
  description = "AWS EC2 instance type tp use for Ollama deployment"
  default     = "c4.2xlarge"
}

variable "aws_resource_tags" {
  description = "A map of tags to add to AWS resources"
  type        = map(string)
  default = {
    Application = "set-genai-workshop5"
  }
}