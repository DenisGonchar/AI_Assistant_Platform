from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.memory import Memory
from app.repositories.memory_repository import MemoryRepository
from app.ai.memory import MemoryExtractor

class MemoryService:
    def __init__(self, db:Session):
        self.repository = MemoryRepository(db)
        self.extractor = MemoryExtractor()
        
    def get_user_memories(self, user_id: int):
        return self.repository.get_user_memories(user_id)
    
    def save_memory(self, user_id: int, content: str) -> Memory | None:
        facts = self.extractor.extract(content)
        for fact in facts:
            if not fact.get('save'):
                continue
            
            content = fact['content'].strip()
            if not content:
                continue
            
            if self.repository.exists(user_id, content):
                continue
            
            memory = Memory(
                user_id=user_id,
                content=content
            )
            
            self.repository.create(memory)
            
    
    def build_prompt(self, user_id: int) -> str:
        memories = self.repository.get_user_memories(user_id)
        if not memories:
            return ""
                
        text = '\n'.join(
            f'- {memory.content}'
            for memory in memories
        )
        
        return f"""
        Вот что известно о пользователе.
        
        {text}
        
        Используй эту информацию,
        если она поможет ответить лучше.
        """
        
    def delete_memory(self, memory_id: int, user_id: int):
        memory = self.repository.get_by_id(memory_id)
        if memory is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Memory not found'
            )
            
        if memory.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Access denied'
            )
            
        self.repository.delete(memory)
        
    