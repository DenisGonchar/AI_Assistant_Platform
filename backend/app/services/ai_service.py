from sqlalchemy.orm import Session

from app.ai.manager import AIManager

from app.services.memory_service import MemoryService
from app.services.web_search_service import WebSearchService
from app.services.decision_service import DecisionService

class AIService:
    def __init__(self, db: Session):
        self.ai = AIManager()
        self.memory_service = MemoryService(db)
        self.web_search_service = WebSearchService()
        self.decision_service = DecisionService()
        
    def generate(self, history: list[dict], user_id: int) -> str:
        
        messages = []
        
        #Memory
        memory_prompt = self.memory_service.build_prompt(user_id)
        
        if memory_prompt:
            messages.append(
                {
                    'role': 'system',
                    'content': memory_prompt
                }
            )
            
        #Web Search
        last_message = next(
            (
                item['content']
                for item in reversed(history)
                if item['role'] == 'user'
            )
        )
        
        if self.decision_service.need_search(last_message):
            search_prompt = self.web_search_service.build_prompt(last_message)
            if search_prompt:
                messages.append(
                    {
                        'role': 'system',
                        'content': search_prompt
                    }
                )
        
        
        #History
        messages.extend(history)
        
        return self.ai.generate(messages)
    
    
    def generate_title(self, message: str) -> str:
        return self.ai.generate_title(message)