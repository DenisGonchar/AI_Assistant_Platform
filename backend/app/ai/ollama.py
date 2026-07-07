import httpx 

from app.ai.base import BaseAI
from app.core.config import settings

class OllamaAI(BaseAI):
    def __init__(self):
        self.url = f"{settings.OLLAMA_URL}/api/chat"
        self.model = settings.OLLAMA_MODEL
        
    def _chat(self, messages: list[dict]) -> str:
        payload = {
            'model': self.model,
            'messages': messages,
            'stream': False    
        }
        
        response = httpx.post(
            self.url,
            json=payload,
            timeout=120
        )
        
        response.raise_for_status()
        
        return response.json()['message']['content'].strip()
        
        
    def generate(self, messages: list[dict]) -> str:
        
        messages = [
            {
                "role": "system",
                "content": (
                    "Ты — AI-помощник. "
                    "Всегда отвечай пользователю на русском языке, "
                    "если он не попросил использовать другой язык."
                ),
            }
        ] + messages
        
        return self._chat(messages)
    
    def generate_title(self, message: str) -> str:
        messages = [
            {
                'role': 'system',
                'content':
                    "Придумай очень короткое название чата.\n"
                    "Максимум 4 слова.\n"
                    "Без кавычек.\n"
                    "Без точки.\n"
                    "Ответь только названием.\n\n"
            },
            {
                'role': 'user',
                'content': message
            },
        ]
        
        return self._chat(messages)
        