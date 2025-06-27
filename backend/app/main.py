from fastapi import FastAPI
from .routes import match_report

app = FastAPI(
    title="Resume-JD Matcher API",
    version="1.0.0"
)
@app.get("/")
async def root():
    return {"message":"Welcome to Resume Parser API"}
app.include_router(match_report.router,prefix="/api",tags=["Match Report"])
