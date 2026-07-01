from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.create_user(user_data)
