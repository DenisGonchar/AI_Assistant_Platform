from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class Chat(Base):
    __tablename__ = 'chats'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    title: Mapped[str] = mapped_column(String(255))
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    user = relationship('User', back_populates='chats')
    
    messages = relationship('Message', back_populates='chat', cascade='all, delete-orphan')

