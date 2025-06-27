# File: backend/app/routes/matching.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.resume_parsing import parse_file_content
from ..services.nlp.generate_match_report import match_report

router = APIRouter()

@router.post("/match-files")
async def create_match_analysis(
    resume: UploadFile = File(..., description="The user's resume file."),
    job_description: UploadFile = File(..., description="The job description file.")
):
    """
    This endpoint orchestrates the entire workflow:
    1. Receives resume and JD files.
    2. Calls the parsing service for each file.
    3. Calls the NLP service with the extracted text.
    4. Returns the final analysis report.
    """
    try:
        # Step 2: Call the parser for each file
        resume_text = await parse_file_content(resume)
        jd_text = await parse_file_content(job_description)

        # Step 3: Call the NLP engine with the extracted text
        analysis_report = match_report(
            job_description=jd_text,
            resume_text=resume_text
        )

        # Step 4: Return the successful report
        return analysis_report

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
