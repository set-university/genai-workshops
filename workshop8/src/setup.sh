#!/bin/bash

sudo apt-get update
sudo apt-get install -y build-essential python3-dev python3-pip
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2004-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic requests streamlit
CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir
pip install langchain pyyaml
docker build -t navigation-assistant .
docker run --gpus all -p 8000:8000 -e HERE_API_KEY=your_api_key navigation-assistant