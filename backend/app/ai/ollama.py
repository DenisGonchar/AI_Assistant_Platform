import httpx 

from app.ai.base import BaseAI
from app.core.config import settings

class OllamaAI(BaseAI):
    def __init__(self):
        self.url = f"{settings.OLLAMA_URL}/api/chat"
        self.model = settings.OLLAMA_MODEL
        
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
        
        payload = {
            'model': self.model,
            'messages': messages,
            'stream': False
        }
        
        try:
            print("URL: ", self.url)
            print("PAYLOAD: ", payload)
            
            response = httpx.post(self.url, json=payload, timeout=300)
            print(response.status_code)
    
            response.raise_for_status()
        
        except httpx.HTTPError as e:
            raise RuntimeError(f'Ollama request failed: {e}') from e
                
        data = response.json()
        
        return data['message']['content']