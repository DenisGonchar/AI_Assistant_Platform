from app.utils.utils import extract_json

from app.ai.manager import AIManager
from app.ai.prompts.decision_prompt import DECISION_PROMPT

class DecisionService:
    def __init__(self):
        self.ai = AIManager()
        
    def need_search(self, message: str) -> bool:
        
        answer = self.ai.generate(
            messages=[{
                'role': 'user',
                'content': message
            }],
            system_prompt=DECISION_PROMPT
            )
        
        print('=== need search ===')
        print(answer)
        
        result = extract_json(answer)
        if isinstance(result, dict):
            return result.get('search', False)
        
        return False
    