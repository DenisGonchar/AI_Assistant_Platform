import httpx 

from app.ai.base import BaseAI
from app.core.config import settings

from app.ai.prompts.assistant_prompt import ASSISTANT_PROMPT
from app.ai.prompts.title_prompt import TITLE_PROMPT

class OllamaAI(BaseAI):
    def __init__(self):
        self.url = f"{settings.OLLAMA_URL}/api/chat"
        self.model = settings.OLLAMA_MODEL
        
    def _chat(self, messages: list[dict]) -> str:
        payload = {
            'model': self.model,
            'messages': messages,
            'stream': False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_predict": 512,
            }    
        }
        
        response = httpx.post(
            self.url,
            json=payload,
            timeout=120
        )
        
        response.raise_for_status()
        
        return response.json()['message']['content'].strip()
        
        
    def generate(self, messages: list[dict], system_prompt: str | None = None) -> str:
        
        if system_prompt:
            final_messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]
        else:
            final_messages = [
                {
                    "role": "system",
                    "content": ASSISTANT_PROMPT
                }
            ]
        
        final_messages.extend(messages)
        
        return self._chat(final_messages)
    
    def generate_title(self, message: str) -> str:
        messages = [
            {
                'role': 'system',
                'content': TITLE_PROMPT
            },
            {
                'role': 'user',
                'content': message
            },
        ]
        
        return self._chat(messages)
        