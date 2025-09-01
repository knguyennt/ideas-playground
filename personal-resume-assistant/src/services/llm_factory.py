from dotenv import load_dotenv
import os
from pathlib import Path
from .openai_provider import OpenAIProvider
from .openllm_provider import OpenLLMProvider
from .llm_service import LLMStrategy

# Get the project root directory (go up from src/services/ to project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

class LLMFactory:    
    @staticmethod
    def create_provider(provider_type: str = None) -> LLMStrategy:
        if provider_type is None:
            provider_type = os.getenv('LLM_PROVIDER')
        
        provider_type = provider_type.lower()
        
        if provider_type == "openai":
            return OpenAIProvider()
        elif provider_type == "openllm":
            return OpenLLMProvider()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_type}. Supported providers: 'openai', 'openllm'")
    
    @staticmethod
    def get_available_providers() -> list[str]:
        return ["openai", "openllm"]