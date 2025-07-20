# File: backend/app/routes/matching.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.resume_parsing import parse_file_content
from ..services.nlp.context_keyword_extraction import extract_relevant_skills_and_keywords
from ..services.ats_scoring import content_quality_points, formatting_points, keyword_points, context_or_relevance_points, section_points

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
        # Step 2: Call the parser for each file
    resume_text = await parse_file_content(resume)
    jd_text = await parse_file_content(job_description)

    # split the resume text into sections and extract job description keywords
    sections=context_or_relevance_points.split_into_sections(resume_text)
    jd_keywords = extract_relevant_skills_and_keywords(jd_text)


    # keyword matching score and suggestions
    keyword_score,missing_keywords,keyword_feedback=keyword_points.compute_keyword_score_and_suggestions(jd_text, resume_text)

    # standard section score and feedback 
    section_score, section_feedback=section_points.section_completion(resume_text)

    # content quality score and feedback
    content_quality_score, content_quality_feedback = content_quality_points.content_quality_score_and_suggestions(resume_text)

    # formatting score and feedback
    formatting_score, formatting_feedback = formatting_points.formatting_score_and_suggestions(resume)

    # context or relevance score and feedback
    context_score, context_feedback = context_or_relevance_points.keyword_context_points(sections, jd_keywords)

    overall_score = keyword_score + section_score + content_quality_score + formatting_score + context_score

    overall_feedback = "Resume are considered ATS-friendly if the score is greater than 80"

    result =[
        {
            "type": "Total ATS score",
            "score": overall_score,
            "suggestions" : overall_feedback
        },

        { 
            "type":"keyword match",
            "score": keyword_score,
            "missing_keywords": missing_keywords,
            "suggestions": keyword_feedback
        },
        { 
            "type":"standard section match",
            "score": section_score,
            "suggestions": section_feedback

        },
        { 
            "type":"formatting match",
            "score": formatting_score,
            "suggestions": formatting_feedback

        },
        { 
            "type":"content quality",
            "score": content_quality_score,
            "suggestions": content_quality_feedback

        },
        { 
            "type":"context or relevance",
            "score": context_score,
            "suggestions": context_feedback

        }
        
        
    ]


       

        

        # Step 4: Return the successful report
    return result
