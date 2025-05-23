# File Q&A with Claude 3.5 Sonnet

This Streamlit application allows users to upload text files and ask questions about their content using Amazon Bedrock's Claude 3.5 Sonnet model.

## Prerequisites

- AWS Account with Bedrock access
- AWS CLI configured with credentials (`aws configure`)
- Claude 3.5 Sonnet model enabled in your AWS account

## Installation

1. Install Conda:
   - **Windows**: 
     - Download [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
     - Run the installer (.exe file)
   - **macOS**:
     ```bash
     brew install --cask miniconda
     ```
   - **Linux**:
     ```bash
     wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
     bash Miniconda3-latest-Linux-x86_64.sh
     ```

2. Initialize Conda (macOS/Linux):
   ```bash
   # Add conda to your PATH
   eval "$(/opt/homebrew/Caskroom/miniconda/base/bin/conda shell.bash hook)"
   
   # Initialize conda
   conda init "$(basename "${SHELL}")"
   ```
   
   Close and reopen your terminal after initialization.

## Setup

1. Create a new environment:
```bash
# Remove existing environment if it exists
conda remove --name genai_workshop7 --all

# Create new environment
conda create -n genai_workshop7 python=3.11 -y
```

2. Activate the environment:
```bash
# For macOS/Linux
eval "$(/opt/homebrew/Caskroom/miniconda/base/bin/conda shell.bash hook)"
conda activate genai_workshop7

# For Windows
conda activate genai_workshop7
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Configure AWS credentials (if not already configured):
```bash
aws configure
```
Enter your AWS Access Key ID, Secret Access Key, and preferred region when prompted.

## Running the Application

Run the Streamlit app with:
```bash
streamlit run talk_to_your_file.py
```

## Features

- Upload text (.txt), markdown (.md), or PDF (.pdf) files
- View the extracted content before asking questions
- Ask questions about the uploaded content
- Get AI-powered responses using Claude 3.5 Sonnet

## Usage

1. Upload a text file
2. Type your question about the content
3. Get an AI-generated response

## Security Note

The application uses your AWS credentials from the AWS CLI configuration. Make sure your credentials are stored securely and have the appropriate permissions for Amazon Bedrock.

## Troubleshooting

If you encounter issues with Conda:

### macOS
- If conda command is not found:
  ```bash
  eval "$(/opt/homebrew/Caskroom/miniconda/base/bin/conda shell.bash hook)"
  ```
- If you get "source: no such file or directory: activate":
  ```bash
  # First add conda to PATH
  eval "$(/opt/homebrew/Caskroom/miniconda/base/bin/conda shell.bash hook)"
  
  # Then initialize
  conda init "$(basename "${SHELL}")"
  
  # Close and reopen terminal, then activate
  conda activate genai_workshop7
  ```

### Windows
- Make sure to run commands in Anaconda Prompt
- If you get initialization errors, run:
  ```bash
  conda init
  ```
  Then close and reopen Anaconda Prompt
