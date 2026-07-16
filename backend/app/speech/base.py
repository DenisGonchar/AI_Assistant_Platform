from abc import ABC, abstractmethod

class BaseSpeech(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> str:
        pass