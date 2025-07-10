import re

def content_quality_score(resume_text: str, max_points=15):
    """
    Scores the content quality of a resume based on quantified achievements,
    action verbs, spelling, and placeholder text.

    Args:
        resume_text (str): The plain text of the resume.
        max_points (int): Maximum points for content quality.

    Returns:
        tuple: (score, list of content quality feedback)
    """
    deductions = 0
    feedback = []

    # 1. Check for quantified achievements (numbers, %, $)
    quantified = re.findall(r'\b\d+(\.\d+)?(%|\$|k|K|m|M)?\b', resume_text)
    if not quantified:
        deductions += 5
        feedback.append("Add quantified achievements (e.g., numbers, percentages, or metrics) to strengthen your resume.")

    # 2. Check for action verbs (at least a few)
    action_verbs = [
        "achieved", "managed", "led", "developed", "designed", "implemented",
        "improved", "created", "increased", "reduced", "launched", "built",
        "organized", "coordinated", "analyzed", "delivered", "presented"
    ]
    action_verbs_found = [verb for verb in action_verbs if re.search(rf'\b{verb}\b', resume_text, re.IGNORECASE)]
    if len(action_verbs_found) < 3:
        deductions += 4
        feedback.append("Use more action verbs (e.g., led, developed, achieved) to describe your experience.")

    # 3. Check for placeholder text
    if re.search(r'lorem ipsum|dummy text|your name here', resume_text, re.IGNORECASE):
        deductions += 3
        feedback.append("Remove placeholder text like 'lorem ipsum' or 'your name here'.")

    # 4. Basic spell check (very basic, for MVP)
    # Here we'll just flag if there are many words with no vowels (a crude check)
    words = resume_text.split()
    suspicious_words = [w for w in words if len(w) > 4 and not re.search(r'[aeiouAEIOU]', w)]
    if len(suspicious_words) > 10:
        deductions += 2
        feedback.append("Check for possible spelling mistakes or typos.")

    score = max(max_points - deductions, 0)
    if not feedback:
        feedback.append("Your resume content is clear, quantified, and action-oriented!")

    return score, feedback

