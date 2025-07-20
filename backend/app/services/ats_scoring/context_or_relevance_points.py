import re

def split_into_sections(resume_text: str):
    """
    Split the resume text into sections based on standard section headers.
    Args:
        resume_text (str): The resume text.
    Returns:
        dict: A dictionary with section names as keys and their corresponding text as values.
    """
    section_headers = [
        r"(?i)^\s*(contact|contact information|contact info)\s*?:",
        r"(?i)^\s*(profile|summary|professional summary|about me|objective):\s*?",
        r"(?i)^\s*(education|academic background|educational qualification):\s*?",
        r"(?i)^\s*(experience|work experience|professional experience|employment history):\s*?",
        r"(?i)^\s*(skills|technical skills|core competencies):\s*?",
        r"(?i)^\s*(projects|project experience):\s*?",
        r"(?i)^\s*(certifications|certificates):\s*?"
    ]
    matches = []
    for pattern in section_headers:
        for m in re.finditer(pattern, resume_text, flags=re.MULTILINE):
            matches.append((m.start(), m.end(), m.group(1).strip().lower()))
    matches.sort(key=lambda x: x[0])

    if not matches:
        return {"other": resume_text.strip()}
    sections = {}
    for i, (start, end, section_name) in enumerate(matches):
        content_start = end
        content_end = matches[i+1][0] if i+1 < len(matches) else len(resume_text)
        section_content = resume_text[content_start:content_end].strip()
        sections[section_name] = section_content
    return sections

def keyword_context_points(sections: dict, jd_keywords: list, max_points=10) -> tuple:
    """
    Calculate context points based on presence of job description keywords in standard sections.
    Args:
        sections (dict): A dictionary of section names and their content.
        jd_keywords (list): A list of keywords from the job description.
        max_points (int): Maximum possible points for context scoring.
    Returns:
        tuple: (score, feedback)
    """
    found_in_context = set()
    found_in_skills = set()
    missing = set()
    context_sections = {"projects", "experience", "work experience", "professional experience"}
    skill_sections = {"skills", "technical skills", "core competencies"}
    sections = {k.lower(): v.lower() for k, v in sections.items()}
    for kw in jd_keywords:
        kw = kw.lower()
        found = False
        # Check context sections
        for sec in context_sections:
            if sec in sections and re.search(rf"\b{re.escape(kw)}\b", sections[sec]):
                found = True
                found_in_context.add(kw)
                break
        # Check skills sections only if not found in context
        if not found:
            for sec in skill_sections:
                if sec in sections and re.search(rf"\b{re.escape(kw)}\b", sections[sec]):
                    found_in_skills.add(kw)
                    found = True
                    break
        if not found:
            missing.add(kw)
    # Scoring: prioritize context matches
    total = len(jd_keywords)
    context_score = len(found_in_context) / total if total else 0
    skills_score = len(found_in_skills) / total if total else 0
    score = max_points * (0.7 * context_score + 0.3 * skills_score)

    # Feedback
    feedback = []
    if found_in_skills:
        feedback.append(f"Some skills ({', '.join(sorted(found_in_skills))}) are only listed in Skills. Add them to Experience/Projects for more impact.")
    if found_in_context:
        feedback.append(f"Great! You have contextualized these key skills: {', '.join(sorted(found_in_context))}.")
    if not found_in_context and not found_in_skills:
        feedback.append("No relevant skills from the job description found. Tailor your resume more closely to the JD.")
    return score, feedback

