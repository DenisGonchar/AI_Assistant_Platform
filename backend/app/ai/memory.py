from app.ai.manager import AIManager
from app.utils.utils import extract_json

from app.ai.prompts.memory_prompt import MEMORY_PROMPT

class MemoryExtractor:
    def __init__(self):
        self.ai = AIManager()
        
    def extract(self, message: str) -> list[str]:
        answer = self.ai.generate(
            messages=[
                {
                    'role': 'user',
                    'content': message
                }
            ],
            system_prompt=MEMORY_PROMPT
            )
        
        print('=== extract ===')
        print(answer)
        
        data = extract_json(answer)
        if not isinstance(data, list):
            return []
        
        print('data: \n', data)
        return data