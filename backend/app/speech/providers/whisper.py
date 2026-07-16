from faster_whisper import WhisperModel

from app.speech.base import BaseSpeech
from app.core.config import settings

class WhisperSpeech(BaseSpeech):
    def __init__(self):
        self.model = WhisperModel(
            settings.WHISPER_MODEL,
            device=settings.WHISPER_DEVICE,
            compute_type=settings.WHISPER_COMPUTE_TYPE
            
        )
    
    def transcribe(self, audio_path: str) -> str:
        segments, info = self.model.transcribe(audio_path)
        
        text = ''
        
        for segment in segments:
            text += segment.text
            
        return text.strip()