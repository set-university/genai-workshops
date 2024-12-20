locals {
  vpc_cidr  = "10.0.0.0/16"
  azs = slice(data.aws_availability_zones.available.names, 0, 3)
  user_data = <<-EOT
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y gcc kernel-devel-$(uname -r)
              aws s3 cp --recursive s3://ec2-linux-nvidia-drivers/latest/ .
              chmod +x NVIDIA-Linux-x86_64*.run
              mkdir /home/ec2-user/tmp
              chmod -R 777 tmp
              export TMPDIR=/home/ec2-user/tmp
              CC=/usr/bin/gcc10-cc ./NVIDIA-Linux-x86_64*.run --tmpdir=$TMPDIR
              sudo touch /etc/modprobe.d/nvidia.conf
              echo "options nvidia NVreg_EnableGpuFirmware=0" | sudo tee --append /etc/modprobe.d/nvidia.conf
              sudo yum install -y docker git
              sudo usermod -a -G docker ec2-user
              sudo systemctl enable docker.service
              sudo systemctl start docker.service
              curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo | \
                sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
              sudo yum install -y nvidia-container-toolkit
              sudo nvidia-ctk runtime configure --runtime=docker
              sudo systemctl restart docker
              sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose
              docker-compose version
              git clone https://github.com/ollama-webui/ollama-webui
              cd ollama-webui
              docker-compose up -d
              EOT
}