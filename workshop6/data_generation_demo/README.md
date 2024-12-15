# Data Generation and Review Demo

This is a **Gradio-based web application** that allows users to generate synthetic product data or create reviews and ratings based on existing product data using the **OpenAI API**.

---

## Features

1. **Generate Product Data**  
   - Automatically generate product data samples in a CSV format.
   - Users can specify the number of samples.

2. **Generate Reviews and Ratings**  
   - Upload a CSV file containing product data.
   - The app processes the file and generates reviews and ratings for the products.

3. **Download Generated Data**  
   - Generated product data or reviews can be downloaded as a CSV file.

---

## Docker Setup Guide

### 1. Build the Docker Image

Make sure Docker is installed on your machine. Then run the following command to build the image:

```bash
docker build -t data-generation-demo .
```

### 2. Run the Docker Container

To start the container and expose the Gradio app on port `7860`, use the following command:

```bash
docker run -p 7860:7860 --e OPENAI_API_KEY=<your-openai-api-key> data-generation-demo
```

Replace `<your-openai-api-key>` with your valid OpenAI API key.

---

## Running the App

### Locally (without Docker)
```bash
export OPENAI_API_KEY=<your-openai-api-key>
python app.py
```

### Using Docker
```bash
docker run -p 7860:7860 --env OPENAI_API_KEY=<your-openai-api-key> data-generation-demo
```

The app will be available at `http://localhost:7860` in your browser.

---

## How to Use the App

1. **Select an Action:**
   - "Generate Product Data" to create synthetic product data.
   - "Generate Reviews" to upload existing product data and get reviews.

2. **For Product Data Generation:**
   - Enter the number of samples to generate.
   - Click **Submit** to generate the data.
   - Download the generated CSV file.

3. **For Review Generation:**
   - Upload a CSV file of product data (must have appropriate columns like product names).
   - Click **Submit** to generate reviews and ratings.
   - Download the generated reviews CSV.