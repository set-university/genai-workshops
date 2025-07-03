locals {
  vpc_cidr  = "10.0.0.0/16"
  azs       = slice(data.aws_availability_zones.available.names, 0, 3)
  user_data = <<-EOT
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y gcc kernel-devel-$(uname -r)
              mkdir /home/ec2-user/tmp
              chmod -R 777 tmp
              export TMPDIR=/home/ec2-user/tmp
              sudo yum install -y docker git
              sudo usermod -a -G docker ec2-user
              sudo systemctl enable docker.service
              sudo systemctl start docker.service
              sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose
              docker-compose version
              git clone https://github.com/ollama-webui/ollama-webui
              cd ollama-webui
              docker-compose up -d
              EOT
}