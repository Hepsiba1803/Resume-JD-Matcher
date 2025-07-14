import re
def content_quality_score_and_suggestions(resume_text: str, max_points=15):
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
        feedback.append("Add metrics. Numbers, percentages, and data help quantify your impact.")

    # 2. Check for action verbs (at least a few)
    action_verbs = [
        "achieved", "managed", "led", "developed", "designed", "implemented",
        "improved", "created", "increased", "reduced", "launched", "built",
        "organized", "coordinated", "analyzed", "delivered", "presented"
    ]
    action_verbs_found = [verb for verb in action_verbs if re.search(rf'\b{verb}\b', resume_text, re.IGNORECASE)]
    if len(action_verbs_found) < 3:
        deductions += 4
        feedback.append("Use strong action verbs like 'led', 'developed', or 'delivered' to convey ownership.")

    # 3. Check for placeholder text
    if re.search(r'lorem ipsum|dummy text|your name here', resume_text, re.IGNORECASE):
        deductions += 3
        feedback.append("Remove any placeholder content—make sure everything speaks to your real experience.")

    # 4. Basic spell check (very basic)
    words = resume_text.split()
    suspicious_words = [w for w in words if len(w) > 4 and not re.search(r'[aeiouAEIOU]', w)]
    if len(suspicious_words) > 10:
        deductions += 2
        feedback.append("Review for possible spelling mistakes or typos. A quick proofread can go a long way.")

    score = max(max_points - deductions, 0)
    if not feedback:
        feedback.append("Nicely done! Your resume content is clear, focused, and results-driven.")

    return score, feedback
