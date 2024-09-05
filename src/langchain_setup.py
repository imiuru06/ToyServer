import json
import os
import requests
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain

# 환경 변수 로드
load_dotenv()

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as file:
        return json.load(file)

def create_tool_chain(model_name, provider):
    """Create a LangChain tool for interacting with OpenAI or Azure OpenAI."""
    
    if provider == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables.")
        openai_llm = OpenAI(api_key=api_key, model_name=model_name)
        
        def call_openai_tool(prompt):
            response = openai_llm(prompt=prompt)
            return response['choices'][0]['text'].strip()
    
        return lambda prompt: call_openai_tool(prompt)
    
    elif provider == 'azure':
        azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        azure_api_key = os.getenv('AZURE_OPENAI_API_KEY')
        deployment_id = os.getenv('AZURE_OPENAI_DEPLOYMENT_ID')  # 배포 ID를 환경 변수로 추가

        if not azure_endpoint or not azure_api_key or not deployment_id:
            raise ValueError("AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, or AZURE_OPENAI_DEPLOYMENT_ID not set in environment variables.")
        
        def call_azure_tool(prompt):
            headers = {
                'Content-Type': 'application/json',
                'api-key': azure_api_key
            }
            payload = {
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.7,
                'top_p': 0.95,
                'max_tokens': 800
            }
            url = f'{azure_endpoint}/openai/deployments/{deployment_id}/chat/completions?api-version=2024-02-15-preview'
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                return response_data['choices'][0]['message']['content'].strip()
            else:
                response.raise_for_status()  # Raise an exception for HTTP errors
        
        return lambda prompt: call_azure_tool(prompt)
    
    else:
        raise ValueError("Unsupported provider: Only 'openai' and 'azure' are supported.")

def setup_langchain():
    """Setup LangChain with configuration from a JSON file."""
    config = load_config('config.json')
    model_name = config['model_name']
    provider = config['provider']
    tool_chain = create_tool_chain(model_name, provider)
    return tool_chain
