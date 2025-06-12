import streamlit as st
import os
import re 

from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from parsers.txt_parser import extract_text_from_txt

from extractors.skills_extractor import extract_skills
from extractors.education_extractor import extract_education
from extractors.section_validator import validate_sections
from extractors.experience_extractor import extract_years_of_experience
from extractors.soft_skills_extractor import extract_soft_skills
from extractors.jobtitle_extractor import job_title_score
from extractors.location_extractor import location_score

from scoring.overall_score import calculate_ats_score
from scoring.semantic_scoring import semantic_similarity
from scoring.formatting_scoring import formatting_score
from scoring.keyword_scoring import keyword_score

soft_skills_list = [
    "communication", "teamwork", "problem-solving", "leadership", "adaptability",
    "creativity", "work ethic", "time management", "attention to detail", "interpersonal skills",
    "self-motivation", "decision-making", "organization", "flexibility", "conflict resolution"
]

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ATS Resume Scoring System",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR COLORS AND FONTS ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #43e97b 0%, #38f9d7 100%) !important;
    }
    .stApp {
        background: linear-gradient(120deg, #43e97b 0%, #38f9d7 100%) !important;
    }
    .big-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg,#764ba2,#667eea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5em;
    }
    .score-badge {
        display: inline-block;
        padding: 0.5em 1.2em;
        border-radius: 2em;
        background: linear-gradient(90deg,#43e97b,#38f9d7);
        color: #fff;
        font-size: 1.5em;
        font-weight: 800;
        box-shadow: 0 4px 24px rgba(76,34,158,0.14);
        margin-bottom: 1em;
    }
    .stButton>button {
        background: linear-gradient(90deg,#764ba2,#43e97b);
        color: #fff;
        font-weight: 700;
        border: none;
        border-radius: 1.5em;
        padding: 0.6em 2em;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg,#38f9d7,#764ba2);
        color: #222;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="big-title"> ATS Resume Scoring System</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:black;'>Upload your resume and paste the job description to see your ATS score and insights. Stand out in your job search with data-driven feedback!</p>",
    unsafe_allow_html=True
)

# --- INPUTS ---
col1, col2 = st.columns([1,2])
col1, col2 = st.columns(2)

with col1:
    st.markdown("<label style='color:black; font-weight:bold;'>Upload Resume</label>", unsafe_allow_html=True)
    resume_file = st.file_uploader("", type=['pdf', 'docx', 'txt'])

with col2:
    st.markdown("<label style='color:black; font-weight:bold;'>Paste Job Description</label>", unsafe_allow_html=True)
    job_desc = st.text_area("", height=140)


# --- ANALYZE BUTTON ---
analyze_btn = st.button("🔍 Analyze Resume", use_container_width=True)

if analyze_btn:
    if resume_file and job_desc.strip():
        with st.spinner("Analyzing your resume..."):
            uploads_dir = "uploads"
            os.makedirs(uploads_dir, exist_ok=True)
            file_path = os.path.join(uploads_dir, resume_file.name)
            with open(file_path, "wb") as f:
                f.write(resume_file.getbuffer())

            # Extract text from resume
            if resume_file.name.endswith('.pdf'):
                resume_text = extract_text_from_pdf(file_path)
            elif resume_file.name.endswith('.docx'):
                resume_text = extract_text_from_docx(file_path)
            elif resume_file.name.endswith('.txt'):
                resume_text = extract_text_from_txt(file_path)
            else:
                st.error("Unsupported file format.")
                st.stop()

            jd_keywords = job_desc.lower().split()

            # Extract job title and location from job description
            target_job_title = ""
            for line in job_desc.split('\n'):
                if line.strip():
                    target_job_title = line.strip()
                    break

            job_location = ""
            for line in job_desc.lower().split('\n'):
                if 'location' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        job_location = parts[1].strip()
                    else:
                        job_location = line.replace('location', '').strip()
                    break

            try:
                skills = extract_skills(resume_text, jd_keywords)
                education = extract_education(resume_text)
                sections = validate_sections(resume_text)
                years_exp = extract_years_of_experience(resume_text)
                soft_skills = extract_soft_skills(resume_text, soft_skills_list)
                semantic_score = semantic_similarity(resume_text, job_desc)
                formatting = formatting_score(resume_text)
                keyword_metrics = keyword_score(resume_text, jd_keywords)
            except Exception as e:
                st.error(f"Error during extraction: {e}")
                os.remove(file_path)
                st.stop()

            required_years = 2
            experience_score = min(years_exp / required_years, 1.0) if required_years else 0

            metrics = {
                'skills': len(skills) / len(set(jd_keywords)) if jd_keywords else 0,
                'semantic': semantic_score,
                'sections': sum(sections.values()) / len(sections) if sections else 0,
                'experience': experience_score,
                'education': 1 if education else 0,
                'soft_skills': len(soft_skills) / len(soft_skills_list) if soft_skills_list else 0,
                'job_title': job_title_score(resume_text, target_job_title),
                'location': location_score(resume_text, job_location),
            }

            ats_score = calculate_ats_score(metrics)

            st.markdown(f'<div class="score-badge">Your ATS Score: {int(ats_score)}%</div>', unsafe_allow_html=True)

            colA, colB = st.columns(2)
            with colA:
                st.markdown("### 🎯 **Matched Skills**")
                st.success(", ".join(skills) if skills else "No skills matched.")
                st.markdown("### 🎓 **Education Found**")
                st.info(education if education else "No education found.")
                st.markdown("### 🏆 **Soft Skills Detected**")
                st.success(", ".join(soft_skills) if soft_skills else "No soft skills detected.")

            with colB:
                st.markdown("### 📑 **Section Completion**")
                st.write(sections)
                st.markdown("### ⏳ **Years of Experience**")
                st.info(str(years_exp))
                st.markdown("### 🖋️ **Formatting Score**")
                st.write(formatting)
                st.markdown("### 🔑 **Keyword Metrics**")
                st.write(keyword_metrics)

            os.remove(file_path)
    else:
        st.warning("Please upload a resume and paste a job description.")
