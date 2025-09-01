from .llm_service import LLMStrategy
from openai import OpenAI

class OpenAIProvider(LLMStrategy):
    def __init__(self):
        self._client = OpenAI(base_url="", api_key="")

        if (LLMStrategy.system_prompt):
            self._client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": LLMStrategy.system_prompt}
                ]
            )

    def generate_response(self, prompt: str, history: list) -> str:
        response = self._client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            history=history
        )
        return response.choices[0].message.content