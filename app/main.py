from fastapi import FastAPI
from app.core.config import APP_NAME, APP_VERSION
from app.core.database import engine, Base
from app.models import user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description="AI-powered coaching center management platform",
    version=APP_VERSION
)

@app.get("/")
def home():
    return {
        "platform": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }