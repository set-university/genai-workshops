
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir
COPY . .
RUN mkdir -p /app/models
ENV MODEL_PATH=/app/models/Mistral-7B-Instruct-v0.3.Q8_0.gguf
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]