from sqlalchemy.orm import Session

from app.models.message import Message
from app.repositories.message_repository import MessageRepository
from app.database.enums import MessageRole
from app.ai.memory import MemoryExtractor

from app.services.chat_service import ChatService
from app.services.ai_service import AIService
from app.services.memory_service import MemoryService


class MessageService:
    def __init__(self, db: Session):
        self.message_repository = MessageRepository(db)
        self.chat_service = ChatService(db)
        self.memory_service = MemoryService(db)
        
        self.ai = AIService()
        
        self.memory_extractor = MemoryExtractor()
        
    def send_message(self, chat_id: int, user_id: int, content:str):
        
        #Проверка, что чат существует и принадлежит пользователю
        self.chat_service.get_chat(chat_id, user_id)
        
        #сохраняем сообщения пользователя
        user_message = Message(
            chat_id=chat_id,
            role=MessageRole.USER,
            content=content
            )
        
        self.message_repository.create(user_message)
        
        #сохраняем в память длительную информацию
        self.memory_service.save_memory(user_id, content)
        
        #Строим промпт памяти
        memory_prompt = self.memory_service.build_prompt(user_id)
        
        #Получаем историю сообщений
        messages = self.message_repository.get_chat_messages(chat_id)
        
        #Генерируем заголовок чата
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
        
        #Генерируем ответ
        answer = self.ai.generate(history, memory_prompt)
        
        #сохраняем сообщения модели
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
    
    