from .keyword_extraction import extract_keywords
from .match_score import match_score
 
def match_report(job_description: str, resume_text: str) -> dict:
    """
    Generate a match report comparing a job description with a resume.

    Args:
        job_description (str): The job description text.
        resume_text (str): The resume text.

    Returns:
        dict: A dictionary containing the match score and keywords.
    """
    # Extract keywords from both job description and resume
    jd_keywords = extract_keywords(job_description)
    resume_keywords =extract_keywords(resume_text)
    jd_keywords_str= " ".join(jd_keywords)
    resume_keywords_str =" ".join(resume_keywords)
    # calculate match score
    match_score_value = match_score(job_description, resume_text)
    if match_score_value is None:
        return {"message": "Match score is None. Please check the input texts"}
    else:
        return {
            "match_score": round(match_score_value*100,2),
            "jd_keywords": sorted(list(jd_keywords)),
            "resume_keywords": sorted(list(resume_keywords))
        }
    
    