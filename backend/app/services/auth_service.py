from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.security.password import verify_password

class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        
    def login(self, data: LoginRequest):
        user = self.repository.get_by_email(data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        access_token = create_access_token({"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}