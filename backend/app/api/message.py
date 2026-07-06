from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService

router = APIRouter(
    prefix='/chats',
    tags=['Messages']
)

@router.post(
    '/{chat_id}/messages',
    response_model=MessageResponse
)
def send_message(chat_id: int, data: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = MessageService(db)
    return service.send_message(chat_id=chat_id, user_id=current_user.id, content=data.content)


@router.get(
    '/{chat_id}/messages',
    response_model=list[MessageResponse]
    )
def get_messages(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = MessageService(db)
    return service.get_messages(chat_id, current_user.id)