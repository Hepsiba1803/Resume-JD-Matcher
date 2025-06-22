from fastapi import FastAPI
from app.routes import upload_resume

app = FastAPI()
app.include_router(upload_resume.router,prefix="/api", tags=["Resume Upload"])