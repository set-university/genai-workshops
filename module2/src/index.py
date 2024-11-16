import boto3
import os

client = boto3.client('bedrock-agent-runtime')


def handler(event, context):
    prompt = event['body']['prompt']
    response = client.retrieve_and_generate(
        input={
            'text': prompt
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': os.getenv('BEDROCK_KB_ID'),
                'modelArn': os.getenv('GEN_AI_MODEL_ARN')
            },
            'type': 'KNOWLEDGE_BASE'
        }
    )
    return response
