from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.auth.dependencies import get_current_user

from app.schemas.memory import MemoryResponse
from app.services.memory_service import MemoryService

router = APIRouter(
    prefix='/memories',
    tags=['Memory']
)

@router.get('', response_model=list[MemoryResponse])
def get_memories(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MemoryService(db)
    return service.get_user_memories(current_user.id)

@router.delete('/{memory_id}', status_code=204)
def delete_memory(memory_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MemoryService(db)
    service.delete_memory(memory_id, current_user.id)
