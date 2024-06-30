from LLMs import LLM_model
from config import GPT_API

def get_llm_model():
    llm_instance = LLM_model.LLMModel(openai_api_key=GPT_API, temperature=0.1)
    return llm_instance.get_llm_model()