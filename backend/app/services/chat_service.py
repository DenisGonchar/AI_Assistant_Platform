from app.models.chat import Chat
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatCreate

class ChatService:
    def __init__(self, repository: ChatRepository):
        self.repository = repository
        
    def create_chat(self, data: ChatCreate, user_id: int)->Chat:
        
        title = data.title.strip()
        
        if not title:
            title = "New chat"
            
        chat = Chat(
            title=title,
            user_id=user_id
        )
        
        return self.repository.create(chat)
    
    def get_user_chats(self, user_id: int):
        return self.repository.get_all_by_user(user_id)