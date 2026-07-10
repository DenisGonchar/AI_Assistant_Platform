from app.ai.manager import AIManager

class AIService:
    def __init__(self):
        self.manager = AIManager()
        
    def generate(self, history: list[dict], memory: str = '') -> str:
        return self.manager.generate(history, memory)
    
    def generate_title(self, message: str) -> str:
        return self.manager.generate_title(message)