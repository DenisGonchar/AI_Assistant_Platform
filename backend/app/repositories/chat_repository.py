from sqlalchemy.orm import Session

from app.models.chat import Chat

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, chat: Chat)-> Chat:
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat
    
    def update(self, chat: Chat):
        self.db.commit()
        self.db.refresh(chat)
        return chat
    
    def get_by_id(self, chat_id: int) -> Chat | None:
        return self.db.get(Chat, chat_id)
    
    def get_user_chats(self, user_id: int):
        return self.db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.id.desc()).all()
    
    def delete(self, chat: Chat):
        self.db.delete(chat)
        self.db.commit()