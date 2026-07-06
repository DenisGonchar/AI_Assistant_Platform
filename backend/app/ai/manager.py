from app.ai.ollama import OllamaAI


class AIManager:
    def __init__(self):
        self.provider = OllamaAI()
        
    def generate(self, messages: list[dict]) -> str:
        return self.provider.generate(messages)
    
    def generate_title(self, message: str) -> str:
        return self.provider.generate_title(message)