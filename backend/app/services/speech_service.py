from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import UploadFile, HTTPException

from app.core.config import settings
from app.speech.manager import SpeechManager

ALLOWED_AUDIO_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp3",
    "audio/ogg",
    "audio/webm",
    "audio/mp4",
}

class SpeechService:
    def __init__(self):
        self.manager = SpeechManager()
        
    def transcribe(self, file: UploadFile) -> str:
        
        if file.content_type not in ALLOWED_AUDIO_TYPES:
            raise HTTPException(
                status_code=400,
                detail='Unsupported audio format.'
            )
        
        contents = file.file.read()
        if len(contents) > settings.MAX_AUDIO_SIZE:
            raise HTTPException(
                status_code=400,
                detail='Audio file is too large.'
            )
        
        
        temp_dir = Path(settings.TEMP_AUDIO_PATH)
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = temp_dir / f'{uuid4()}.wav'
        
        with open(file_path, 'wb') as buffer:
            buffer.write(contents)
            
        try:
            text = self.manager.transcribe(str(file_path))
        except Exception as e:
            print('-'*20)
            print(f"Speech error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f'Failed to recognize speech.'
            )
        finally:
            if file_path.exists():
                file_path.unlink()
                
        return text