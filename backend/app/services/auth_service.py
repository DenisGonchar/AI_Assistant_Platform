from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.security.password import verify_password

from app.models.user import User
from app.schemas.user import UserCreate
from app.security.password import hash_password

class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def _validate_registration(self, data: UserCreate):
        if self.repository.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if self.repository.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    def _authenticate_user(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
            
            
    def register(self, user_data: UserCreate)-> User:
        self._validate_registration(user_data)
        
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )
        
        return self.repository.create(user)

    def login(self, data: LoginRequest):
        user = self._authenticate_user(data.email, data.password)
        
        access_token = create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=access_token)