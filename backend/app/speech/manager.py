from app.speech.providers.whisper import WhisperSpeech

class SpeechManager:
    def __init__(self):
        self.provider = WhisperSpeech()
        
    def transcribe(self, audio_path: str) -> str:
        return self.provider.transcribe(audio_path)