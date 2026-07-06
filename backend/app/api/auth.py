from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.user import UserResponse
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data)

@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db:Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(data)