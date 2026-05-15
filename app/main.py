from fastapi import FastAPI
from app.core.config import APP_NAME, APP_VERSION
from app.core.database import engine, Base
from app.models import user
from app.api import users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description="AI-powered coaching center management platform",
    version=APP_VERSION
)
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def home():
    return {
        "platform": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }