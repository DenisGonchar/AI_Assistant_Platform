from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository
from app.security.password import hash_password

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        
    def create_user(self, user_data: UserCreate)-> User:
        if self.repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if self.repository.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        

        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )
        
        return self.repository.create(user)