from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.chat import Chat
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatCreate

class ChatService:
    def __init__(self, db: Session):
        self.repository = ChatRepository(db)
        
        
    def create_chat(self, data: ChatCreate, user_id: int)->Chat:
        title =(data.title or '').strip()
        if not title:
            title = 'New chat'
            
        chat = Chat(
            title=title,
            user_id=user_id
        )
        
        return self.repository.create(chat)
    
    def update_title(self, chat_id: int, user_id: int, title: str):
        chat = self.get_chat(chat_id, user_id)
        chat.title = title
        return self.repository.update(chat)
    
    def get_user_chats(self, user_id: int) -> list[Chat]:
        return self.repository.get_user_chats(user_id)
    
    def get_chat(self, chat_id: int, user_id: int) -> Chat:
        chat = self.repository.get_by_id(chat_id)
        
        if chat is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Chat not found'
            )
            
        if chat.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Access denied'
            )
            
        return chat
    
    def delete_chat(self, chat_id: int, user_id: int):
        chat = self.get_chat(chat_id, user_id)
        
        self.repository.delete(chat)