from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os

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

app = FastAPI()

# Allow CORS for all origins (for local dev; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/score-resume/")
async def score_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, resume.filename)
    with open(file_path, "wb") as f:
        f.write(await resume.read())

    # Extract text from resume
    if resume.filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(file_path)
    elif resume.filename.endswith('.docx'):
        resume_text = extract_text_from_docx(file_path)
    elif resume.filename.endswith('.txt'):
        resume_text = extract_text_from_txt(file_path)
    else:
        os.remove(file_path)
        return {"error": "Unsupported file format."}

    jd_keywords = job_description.lower().split()

    # Extract job title and location from job description
    target_job_title = ""
    for line in job_description.split('\n'):
        if line.strip():
            target_job_title = line.strip()
            break

    job_location = ""
    for line in job_description.lower().split('\n'):
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
        semantic_score = semantic_similarity(resume_text, job_description)
        formatting = formatting_score(resume_text)
        keyword_metrics = keyword_score(resume_text, jd_keywords)
        job_title = job_title_score(resume_text, target_job_title)
        location = location_score(resume_text, job_location)
    except Exception as e:
        os.remove(file_path)
        return {"error": f"Error during extraction: {e}"}

    required_years = 2
    experience_score = min(years_exp / required_years, 1.0) if required_years else 0

    metrics = {
        'skills': len(skills) / len(set(jd_keywords)) if jd_keywords else 0,
        'semantic': semantic_score,
        'sections': sum(sections.values()) / len(sections) if sections else 0,
        'experience': experience_score,
        'education': 1 if education else 0,
        'soft_skills': len(soft_skills) / len(soft_skills_list) if soft_skills_list else 0,
        'job_title': job_title,
        'location': location
    }

    ats_score = calculate_ats_score(metrics)

    os.remove(file_path)
    return {
        "ats_score": ats_score,
        "details": {
            "matched_skills": skills,
            "education": education,
            "sections": sections,
            "years_experience": years_exp,
            "soft_skills": soft_skills,
            "formatting": formatting,
            "keyword_metrics": keyword_metrics,
            "job_title_score": job_title,
            "location_score": location
        }
    }
