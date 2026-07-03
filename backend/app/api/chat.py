from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.database.dependencies import get_db

from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatCreate, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)

@router.post('', response_model=ChatResponse)
def create_chat(data: ChatCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = ChatRepository(db)
    service = ChatService(repository)
    return service.create_chat(data, current_user.id)

@router.get('', response_model=list[ChatResponse])
def get_chats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repository = ChatRepository(db)
    service = ChatService(repository)
    return service.get_user_chats(current_user.id)