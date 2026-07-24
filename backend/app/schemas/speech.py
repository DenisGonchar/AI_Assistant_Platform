from pydantic import BaseModel

class SpeechResponse(BaseModel):
    text: str
    
class SpeechChatResponse(BaseModel):
    recognized_text: str
    answer: str