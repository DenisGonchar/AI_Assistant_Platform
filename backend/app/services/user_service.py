from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.security.password import hash_password

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        
   