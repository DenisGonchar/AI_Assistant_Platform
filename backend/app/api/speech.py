from fastapi import APIRouter, UploadFile, File

from app.schemas.speech import SpeechResponse
from app.services.speech_service import SpeechService

router = APIRouter(
    prefix='/speech',
    tags=['Speech']
)

@router.post('/transcribe', response_model=SpeechResponse)
def transcribe(file: UploadFile = File(...)):
    service = SpeechService()
    
    return SpeechResponse(
        text= service.transcribe(file)
    )