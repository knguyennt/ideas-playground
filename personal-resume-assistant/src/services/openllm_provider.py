from .llm_service import LLMStrategy
from openai import OpenAI

class OpenLLMProvider(LLMStrategy):
    def __init__(self):
        self._client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="something")

    def generate_response(self, prompt: str, history: list) -> str:
        messages = history + [{"role": "user", "content": prompt}]
        
        response = self._client.chat.completions.create(
            model="hi",
            messages=messages
        )
        return response.choices[0].message.content