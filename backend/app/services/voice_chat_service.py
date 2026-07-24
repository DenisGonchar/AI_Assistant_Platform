from sqlalchemy.orm import Session

from app.schemas.speech import SpeechChatResponse

from app.services.ai_service import AIService
from app.services.speech_service import SpeechService

class VoiceChatService:
    def __init__(self, db: Session):
        self.ai_service = AIService(db)
        self.speech_service = SpeechService()
        
    def chat(self, audio_file, history: list[dict], user_id: int):
        
        recognized_text = self.speech_service.transcribe(audio_file)
        
        history.append(
            {
                'role': 'user',
                'content': recognized_text
            }
        )
        
        answer = self.ai_service.generate(history, user_id)
        
        result = SpeechChatResponse(
            recognized_text,
            answer
        )
        return result