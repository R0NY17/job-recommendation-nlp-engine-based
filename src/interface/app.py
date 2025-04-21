import streamlit as st
from pathlib import Path

import sys
import os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./src"))  

from src.extraction.pdf_parser import extract_text_from_pdf
from src.extraction.rule_based_parser import parse_resume
from src.matching.semantic_matcher import match_resume_to_jobs_semantic
from src.matching.tfidf_matcher import load_job_descriptions

st.set_page_config(page_title="Resume Matcher", layout="centered")

st.title("Resume Matcher – Job Recommendation Engine")

# Upload PDF
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

st.sidebar.title("Settings")
match_method = st.sidebar.radio(
"Select Matching Method",
("Semantic (BERT)", "TF-IDF"))

top_n = st.sidebar.slider("Number of job matches to display", min_value=1, max_value=10, value=3)

if uploaded_file is not None:
    # Save uploaded file to temp path
    temp_path = Path("data/resumes/temp_resume.pdf")
    temp_path.write_bytes(uploaded_file.read())

    # Extract + parse
    raw_text = extract_text_from_pdf(str(temp_path))
    parsed_resume = parse_resume(raw_text)

    st.subheader("Extracted Resume Info")

    if parsed_resume.get("skills"):
        st.markdown("**Skills:**")
        st.write(", ".join(parsed_resume["skills"]))

    if parsed_resume.get("education"):
        st.markdown("**Education:**")
        st.write(", ".join(parsed_resume["education"]))

    if parsed_resume.get("experience"):
        st.markdown("**Experience:**")
        st.write(", ".join(parsed_resume["experience"]))

    # Load job descriptions
    job_data = load_job_descriptions("data/jobs/job_descriptions.json")

    if match_method == "Semantic (BERT)":
        st.subheader("Top Job Matches (BERT-based Semantic Matching)")
        matches = match_resume_to_jobs_semantic(parsed_resume, job_data, top_n=top_n)
    else:
        from matching.tfidf_matcher import match_resume_to_jobs
        st.subheader("Top Job Matches (TF-IDF Matching)")
        matches = match_resume_to_jobs(parsed_resume, job_data, top_n=top_n)

    # Display results
    for match in matches:
        st.markdown(f"**{match['title']}** — Score: {match['similarity']}")


    # Cleanup
    temp_path.unlink()
