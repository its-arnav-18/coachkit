from fastapi import FastAPI

app = FastAPI(
    title="CoachKit",
    description="AI-powered coaching center management platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "platform": "CoachKit",
        "status": "running",
        "version": "1.0.0"
    }