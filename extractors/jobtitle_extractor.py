import re

def extract_job_titles(resume_text):
    # Simple heuristic: look for lines with common job title keywords
    job_title_keywords = ['engineer', 'developer', 'manager', 'analyst', 'designer', 'consultant']
    lines = resume_text.lower().split('\n')
    found_titles = [line.strip() for line in lines if any(title in line for title in job_title_keywords)]
    return found_titles

def job_title_score(resume_text, target_title):
    found_titles = extract_job_titles(resume_text)
    target_title = target_title.lower()
    for title in found_titles:
        if target_title in title:
            return 1.0  # Full match
    return 0.0  # No match
