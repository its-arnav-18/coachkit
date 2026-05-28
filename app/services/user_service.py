from sqlalchemy.orm import Session
from argon2 import PasswordHasher, exceptions
from app.models.user import User
from app.schemas.user import UserCreate

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        return None
    hashed = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except exceptions.VerifyMismatchError:
        return False
    
def get_all_students(db: Session):
    return db.query(User).filter(User.role == "student").all()

