import pdfplumber
from docx import Document

def check_resume_formatting(file_path: str) -> tuple:
    """
    Check the formatting of the resume to ensure it doesn't contain any images or tables.
    Args:
        file_path (str): The path to the resume file.
    Returns:
        tuple : score, suggestions
    """
    feedback = []
    max_points =15
    deductions =0
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            tables_found=any(page.extract_tables()for page in pdf.pages)
            images_found=any(page.images for page in pdf.pages)
            if tables_found:
                deductions +=5
                feedback.append("Your resume contains tables, which may not be ATS-friendly. Consider removing them.")
            if images_found:
                deductions += 5
                feedback.append("Your resume contains images, which may not be ATS-friendly. Consider removing them.")
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        # check for tables
        if doc.tables:
            deductions += 5
            feedback.append("Your resume contains tables, which may not be ATS-friendly. Consider removing them.")
        # check for images
        if doc.inline_shapes:
            deductions += 5
            feedback.append("Your resume contains images, which may not be ATS-friendly. Consider removing them.")
    formatting_points = max(max_points - deductions,0)
    if not feedback:
        feedback.append("Your resume formatting is ATS-friendly")

    return (formatting_points, feedback)

score_feedback=check_resume_formatting("backend/tests/test_files/sample_resume_image.pdf")
print(score_feedback)
