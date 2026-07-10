from app.ai.manager import AIManager
from app.utils.utils import extract_json

from app.ai.prompts.memory_prompt import MEMORY_PROMPT

class MemoryExtractor:
    def __init__(self):
        self.ai = AIManager()
        
    def extract(self, message: str) -> list[str]:
        prompt = f"""
        {MEMORY_PROMPT}
        {message}
        """
        
        answer = self.ai.generate([
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        print(answer)
        
        data = extract_json(answer)
        if not isinstance(data, list):
            return []
        
        return data