from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session  
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400 , detail="Email already registered")
    return new_user