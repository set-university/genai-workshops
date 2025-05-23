

# Function to simulate a conversation
def get_ai_response(question, llm, prompt, context, history=""):
    from langchain.prompts import PromptTemplate
    
    input_variables=["context", "history", "question"]
    
    # Create prompt template
    prompt_template = PromptTemplate(
        input_variables=input_variables,
        template=prompt
    )
    
    # Format the prompt
    formatted_prompt = prompt_template.format(
        context=context,
        history=history,
        question=question
    )
    
    # Get response
    response = llm(formatted_prompt)
    return response

# Function to simulate a conversation
def get_ai_response_v2(question, llm, prompt, context, history=""):
    from langchain.prompts import PromptTemplate
    from langchain.llms import OpenAI
    
    input_variables=["context", "history", "question"]
    
    # Create prompt template
    prompt_template = PromptTemplate(
        input_variables=input_variables,
        template=prompt
    )
    
    # Format the prompt
    formatted_prompt = prompt_template.format(
        context=context,
        history=history,
        question=question
    )
    
    # Get response
    # Use predict() instead of invoke() for BedrockChat
    response = llm.invoke(formatted_prompt)
    return response


# Function to simulate a conversation
def get_ai_response_secured(question, llm, prompt, context, history=""):
    from langchain.prompts import PromptTemplate
    from langchain.llms import OpenAI
    import uuid

    random_tag = str(uuid.uuid4())
    input_variables=["context", "history", "question", "RANDOM"]

    # Create prompt template
    prompt_template = PromptTemplate(
        input_variables=input_variables,
        template=prompt
    )
    
    # Format the prompt
    formatted_prompt = prompt_template.format(
        context=context,
        history=history,
        question=question,
        RANDOM=random_tag
    )
    
    # Get response
    response = llm(formatted_prompt)
    return response
