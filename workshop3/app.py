import os
from dotenv import load_dotenv
load_dotenv()

import boto3
from langchain_aws import ChatBedrock
from langchain_core.output_parsers import StrOutputParser
from prompts import PROMPTS, LEVEL_PASSWORDS

# Initialize the Bedrock client
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Initialize Bedrock with model from environment
llm = ChatBedrock(
    model_id=os.getenv('MODEL_ID', 'anthropic.claude-v2:1'),
    client=bedrock_client,
    model_kwargs={
        "max_tokens": 1024,
        "temperature": 0.3,
    }
)

class SecuritySystem:
    def __init__(self, level: int = 1):
        self.current_level = level
        self.max_level = 5
        self.chain = self._create_chain(self.current_level)

    def _create_chain(self, level: int):
        prompt = PROMPTS[level]
        return prompt | llm | StrOutputParser()

    def process_input(self, user_input: str) -> tuple[str, bool]:
        """Process user input and return response and level up status"""
        try:
            response = self.chain.invoke({
                "input": user_input,
                "password": LEVEL_PASSWORDS[self.current_level]
            })
            
            level_up = False
            if LEVEL_PASSWORDS[self.current_level] in user_input:
                if self.current_level < self.max_level:
                    level_up = True
                    
            return response, level_up

        except Exception as e:
            return f"Security Protocol Error: {str(e)}", False

    def level_up(self) -> bool:
        """Advance to next level if possible"""
        if self.current_level < self.max_level:
            self.current_level += 1
            self.chain = self._create_chain(self.current_level)
            return True
        return False

    def restart(self):
        """Restart the system at level 1"""
        self.current_level = 1
        self.chain = self._create_chain(self.current_level)

def chat_with_bot():
    print("ATLAS SECURITY SYSTEM")
    print("Type 'quit' to end session or 'restart' to start over")
    print("-" * 50)
    
    security_system = SecuritySystem()
    
    while True:
        print(f"\nCurrent Security Level: {security_system.current_level}")
        user_input = input("\nAgent: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nTerminating secure connection...")
            break
            
        if user_input.lower() == 'restart':
            print("\nRestarting from Level 1...")
            security_system.restart()
            continue
            
        response, level_up = security_system.process_input(user_input)
        print("\nATLAS:", response)
        
        if level_up:
            security_system.level_up()
            print(f"\n[ACCESS GRANTED] - Advancing to Level {security_system.current_level}")
            if security_system.current_level == security_system.max_level:
                print("\n[CONGRATULATIONS] You have completed all security levels!")
                break

if __name__ == "__main__":
    chat_with_bot()
