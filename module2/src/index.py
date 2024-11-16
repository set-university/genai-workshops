import json
import boto3

client = boto3.client('bedrock-agent-runtime')

def handler(event, context):
    prompt = event['body']['prompt']
    response = client.retrieve_and_generate(
        input={
            'text': prompt
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'VVC6N0LJJ9',
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0'
            },
            'type': 'KNOWLEDGE_BASE'
        }
    )
    return response