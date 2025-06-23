from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.resume_parsing import parse_resume

router= APIRouter()

async def upload_resume(resume:UploadFile=File(...)):
    try:
        extracted_text= await parse_resume(resume)
        return {"uploaded_file": resume.filename, "text_preview":extracted_text[:500]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")