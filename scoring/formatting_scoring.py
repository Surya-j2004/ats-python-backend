import re

def is_ats_friendly(resume_text):
    # Check for images, tables, or columns (basic heuristics)
    # In real PDF parsing, you'd check structure, but here we use text-based heuristics
    has_tables = bool(re.search(r'\|.+\|', resume_text))
    has_images = False  # Images usually not present in extracted text
    has_columns = False # Needs PDF structure parsing; simplified here
    return not (has_tables or has_images or has_columns)

def section_completion_score(resume_text):
    required_sections = ['work experience', 'education', 'skills']
    found = [section for section in required_sections if section in resume_text.lower()]
    return len(found) / len(required_sections)

def formatting_score(resume_text):
    ats_friendly = is_ats_friendly(resume_text)
    section_score = section_completion_score(resume_text)
    # Weight: 0.7 for ATS-friendly, 0.3 for section completion
    return 0.7 * int(ats_friendly) + 0.3 * section_score
