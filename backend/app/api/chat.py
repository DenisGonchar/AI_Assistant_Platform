from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.database.dependencies import get_db

from app.schemas.chat import ChatCreate, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)

@router.post('', response_model=ChatResponse)
def create_chat(data: ChatCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.create_chat(data, current_user.id)

@router.get('', response_model=list[ChatResponse])
def get_chats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ChatService(db)
    return service.get_user_chats(current_user.id)

@router.get('/{chat_id}', response_model=ChatResponse)
def get_chat(chat_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.get_chat(chat_id=chat_id, user_id=current_user.id)

@router.delete('/{chat_id}', status_code=204)
def delete_chat(chat_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ChatService(db)
    service.delete_chat(chat_id, current_user.id)