import boto3
import os
import json

client = boto3.client('bedrock-agent-runtime')


def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    prompt = body.get('prompt', 'What is postgres?')
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
    print(response)
    response_body = response.get('output', '{}').get('text', '<Empty text>')
    return {
        'statusCode': 200,
        'body': json.dumps({
            'genai_response': response_body
        })
    }
