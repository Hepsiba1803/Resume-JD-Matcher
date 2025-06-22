from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.resume_parsing import extract_resume_data

router= APIRouter()
@router.post("/upload_resume")
async def upload_resume(resume:UploadFile=File(...)):
    try:
        extracted_text= await extract_resume_data(resume)
        return {"uploaded_file": resume.filename, "text_preview":extracted_text[:500]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")