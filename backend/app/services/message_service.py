from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.ai.manager import AIManager
from app.models.message import Message
from app.repositories.message_repository import MessageRepository
from app.repositories.chat_repository import ChatRepository
from app.database.enums import MessageRole

class MessageService:
    def __init__(self, db: Session):
        self.message_repository = MessageRepository(db)
        self.chat_repository = ChatRepository(db)
        
        self.ai = AIManager()
        
    def send_message(self, chat_id: int, content:str):
        chat = self.chat_repository.get_by_id(chat_id)
        if chat is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Chat",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        user_message = Message(chat_id=chat_id, role=MessageRole.USER, content=content)
        self.message_repository.create(user_message)
        
        messages = self.message_repository.get_chat_messages(chat_id)
        history = [
            {
                'role': message.role.value,
                'content': message.content
            }
            for message in messages
        ]
        
        answer = self.ai.generate(history)
        
        assistant_message = Message(
            chat_id=chat_id,
            role=MessageRole.ASSISTANT,
            content=answer
        )
        
        self.message_repository.create(assistant_message)
        
        return assistant_message