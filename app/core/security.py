from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import SECRET_KEY
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user_email(token: str = Depends(oauth2_scheme)):
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return email

def require_role(required_role: str):
    def role_checker(
        current_user_email: str = Depends(get_current_user_email),
        db: Session = Depends(get_db)
    ):
        from app.services.user_service import get_user_by_email
        user = get_user_by_email(db, current_user_email)
        if user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. {required_role} role required."
            )
        return user
    return role_checker


