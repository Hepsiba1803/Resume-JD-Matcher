from .nlp.context_keyword_extraction import load_skill_set_to_dict
import os


CATEGORY_TEMPLATES = {
    "programming language": (
        "Highlight your proficiency in '{skill}', including relevant projects, coursework, or certifications."
    ),
    "soft skill": (
        "Showcase situations where you demonstrated strong '{skill}' abilities in team or work environments."
    ),
    "technical skill": (
        "Describe how you have applied '{skill}' in practical scenarios, such as projects, internships, or previous roles."
    ),
    "tool": (
        "Mention your experience using '{skill}' as part of your workflow, projects, or daily tasks."
    ),
    "library": (
        "Include examples of how you have utilized the '{skill}' library in your programming work or academic projects."
    ),
    "technology": (
        "Emphasize your familiarity with '{skill}', detailing any hands-on experience, certifications, or significant projects."
    ),
    "other": (
        "Consider adding your experience with '{skill}' if relevant to the job requirements."
    )
}


csv_path = os.path.join(os.path.dirname(__file__), "nlp", "dataset.csv")



category_dictionary = load_skill_set_to_dict(csv_path)

def get_category_for_skill(skill: str) -> str:
    """
    Retrieves the category for a given skill from the category dictionary.

    Args:
        skill (str): The skill for which to retrieve the category.
    Returns:
        str: The category of the skill, or 'other' if not found.
    """
    skill = skill.strip().lower()
    return category_dictionary.get(skill, "other")

def create_suggestion(skill: str) -> str:
    """
    Creates a suggestion for how to include a skill in a resume or job description.

    Args:
        skill (str): The skill for which to create a suggestion.
    Returns:
        str: A formatted suggestion string.
    """
    category = get_category_for_skill(skill).strip().lower()
    # Use the category to get the appropriate template
    template = CATEGORY_TEMPLATES.get(category, CATEGORY_TEMPLATES["other"])
    # Format the template with the skill
    suggestion = template.format(skill=skill.strip().title())
    return suggestion

