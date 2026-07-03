from pydantic import BaseModel, Field

class ChatCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    
    
class ChatResponse(BaseModel):
    id: int
    title: str
    user_id: int
    
    model_config = {
        "from_attributes": True
    }