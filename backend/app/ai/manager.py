from app.ai.ollama import OllamaAI


class AIManager:
    def __init__(self):
        self.provider = OllamaAI()
        
    def generate(self, messages: list[dict]) -> str:
        return self.provider.generate(messages)