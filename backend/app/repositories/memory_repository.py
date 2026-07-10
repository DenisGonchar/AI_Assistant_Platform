from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.memory import Memory

class MemoryRepository:
    def __init__(self, db:Session):
        self.db = db
        
    def create(self, memory: Memory) -> Memory:
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        
        return memory
    
    def exists(self, user_id: int, content: str) -> bool:
        stmt = (select(Memory).where(Memory.user_id == user_id, Memory.content == content))
        return self.db.scalar(stmt) is not None
    
    def get_user_memories(self, user_id: int) -> list[Memory]:
        stmt = (select(Memory).where(Memory.user_id==user_id).order_by(Memory.content))
        return list(self.db.scalars(stmt).all())
        
    def get_by_id(self, memory_id: int):
        return self.db.get(Memory, memory_id)
        
    def delete(self, memory: Memory):
        self.db.delete(memory)
        self.db.commit()