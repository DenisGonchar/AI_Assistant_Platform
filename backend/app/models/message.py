from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.enums import MessageRole

class Message(Base):
    __tablename__ = 'messages'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), default=MessageRole.USER)
    
    content: Mapped[str] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    chat = relationship('Chat', back_populates='messages')