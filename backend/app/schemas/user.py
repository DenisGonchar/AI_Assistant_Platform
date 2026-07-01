import re
from pydantic import BaseModel, EmailStr, Field, field_validator

#Пользователь регестрируется
class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
    )
    
    email: EmailStr
    
    password: str = Field(
        min_length=6,
        max_length=64,
    )
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, username: str) -> str:
        if not re.fullmatch(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return username

    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&_]+$", password):
            raise ValueError('Password must contain at least one lowercase letter, one uppercase letter, and one digit')
        return password


#Для отправки ответа
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    
    model_config = {
        'from_attributes': True
    }