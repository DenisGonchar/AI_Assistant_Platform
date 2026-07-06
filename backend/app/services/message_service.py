from sqlalchemy.orm import Session

from app.ai.manager import AIManager
from app.models.message import Message
from app.repositories.message_repository import MessageRepository
from app.database.enums import MessageRole
from app.services.chat_service import ChatService

class MessageService:
    def __init__(self, db: Session):
        self.message_repository = MessageRepository(db)
        self.chat_service = ChatService(db)
        self.ai = AIManager()
        
    def send_message(self, chat_id: int, user_id: int, content:str):
        
        #Проверка, что чат существует и принадлежит пользователю
        self.chat_service.get_chat(chat_id, user_id)
        
        user_message = Message(
            chat_id=chat_id,
            role=MessageRole.USER,
            content=content
            )
        
        self.message_repository.create(user_message)
        
        messages = self.message_repository.get_chat_messages(chat_id)
        if len(messages) == 1:
            title = self.ai.generate_title(content)
            self.chat_service.update_title(chat_id, user_id, title)
        
        
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
    
    
    def get_messages(self, chat_id: int, user_id: int):
        self.chat_service.get_chat(chat_id, user_id)
        return self.message_repository.get_chat_messages(chat_id)
    
    