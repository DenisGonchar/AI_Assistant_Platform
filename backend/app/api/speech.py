from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User

from app.schemas.speech import SpeechResponse, SpeechChatResponse
from app.services.speech_service import SpeechService

from app.services.voice_chat_service import VoiceChatService

router = APIRouter(
    prefix='/speech',
    tags=['Speech']
)

@router.post('/chat', response_model=SpeechChatResponse)
def speech_chat(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = VoiceChatService(db)
    
    result = service.chat(
        audio_file=file,
        history=[],
        user_id=current_user.id
    )

@router.post('/transcribe', response_model=SpeechResponse)
def transcribe(file: UploadFile = File(...)):
    service = SpeechService()
    
    return SpeechResponse(
        text= service.transcribe(file)
    )