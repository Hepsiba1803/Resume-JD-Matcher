# streamlit_app.py

import streamlit as st
from backend.app.services.resume_parsing import parse_file_content
from backend.app.services.nlp.context_keyword_extraction import extract_relevant_skills_and_keywords
from backend.app.services.ats_scoring import (
    content_quality_points,
    formatting_points,
    keyword_points,
    context_or_relevance_points,
    section_points
)
import spacy
import subprocess

def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()


def run_analysis(resume_file, jd_file):
    # Step 2: parse the uploaded files
    resume_text = parse_file_content(resume_file)
    jd_text = parse_file_content(jd_file)

    # Section splitting + keyword extraction
    sections = context_or_relevance_points.split_into_sections(resume_text)
    jd_keywords = extract_relevant_skills_and_keywords(jd_text)

    # Keyword match score
    keyword_score, missing_keywords, keyword_feedback = keyword_points.compute_keyword_score_and_suggestions(
        jd_text, resume_text
    )

    # Standard section score
    section_score, section_feedback = section_points.section_completion(resume_text)

    # Content quality score
    content_quality_score, content_quality_feedback = content_quality_points.content_quality_score_and_suggestions(
        resume_text
    )

    # Formatting score
    formatting_score, formatting_feedback = formatting_points.formatting_score_and_suggestions(resume_file)

    # Context or relevance score
    context_score, context_feedback = context_or_relevance_points.keyword_context_points(sections, jd_keywords)

    # Overall score
    overall_score = (
        keyword_score + section_score + content_quality_score + formatting_score + context_score
    )
    overall_feedback = "Resumes are considered ATS-friendly if the score is greater than 80."

    result = [
        {"type": "Total ATS score", "score": overall_score, "suggestions": overall_feedback},
        {"type": "Keyword Match", "score": keyword_score, "missing_keywords": missing_keywords, "suggestions": keyword_feedback},
        {"type": "Standard Section Match", "score": section_score, "suggestions": section_feedback},
        {"type": "Formatting Match", "score": formatting_score, "suggestions": formatting_feedback},
        {"type": "Content Quality", "score": content_quality_score, "suggestions": content_quality_feedback},
        {"type": "Context or Relevance", "score": context_score, "suggestions": context_feedback},
    ]

    return result


# Streamlit frontend
st.title("📄 Resume vs JD ATS Matcher")

st.markdown("Upload your resume and job description to analyze how well they match.")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_file = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"])

if st.button("Analyze") and resume_file and jd_file:
    with st.spinner("Running analysis... Please wait ⏳"):
        try:
            results = run_analysis(resume_file, jd_file)
            st.success("✅ Analysis complete!")

            for section in results:
                st.subheader(section["type"])
                st.markdown(f"**Score**: {section['score']}")
                if "suggestions" in section:
                    st.write("💡 Suggestions:")
                    st.write(section["suggestions"])
                if "missing_keywords" in section:
                    st.write("❌ Missing Keywords:")
                    st.write(section["missing_keywords"])
        except Exception as e:
            st.error(f"💥 Error: {e}")
