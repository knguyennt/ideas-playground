from abc import ABC, abstractmethod

class LLMStrategy(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, history: list) -> str:
        pass

class LLMService:
    def __init__(self, strategy: LLMStrategy = None):
        self._strategy = strategy
        self.system_prompt = None

    def set_strategy(self, strategy: LLMStrategy):
        self._strategy = strategy

    def set_system_prompt(self, prompt):
        self.system_prompt = prompt
    
    def generate_response(self, prompt: str, history: list) -> str:
        if not self._strategy:
            raise ValueError("No strategy set")
        
        # If system prompt is set, add it to the beginning of history
        if self.system_prompt:
            # Check if system prompt is already in history to avoid duplication
            if not history or history[0].get("role") != "system":
                history = [{"role": "system", "content": self.system_prompt}] + history
        
        return self._strategy.generate_response(prompt, history)
