module "ollama_ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.7.1"

  name          = "ollama-${random_pet.this.id}"
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.aws_ec2_instance_type

  availability_zone           = module.vpc.azs[0]
  subnet_id                   = module.vpc.public_subnets[0]
  vpc_security_group_ids = [module.security_group.security_group_id]
  create_eip                  = true
  associate_public_ip_address = true

  create_iam_instance_profile = true
  iam_role_description        = "IAM role for Ollama EC2 instance"
  iam_role_policies = {
    AdministratorAccess = "arn:aws:iam::aws:policy/AdministratorAccess"
  }

  root_block_device = [
    {
      volume_size = 100
      volume_type = "gp3"
    }
  ]

  tags = var.aws_resource_tags

  user_data_base64 = base64encode(local.user_data)
  user_data_replace_on_change = true

}