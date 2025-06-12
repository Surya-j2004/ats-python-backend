def validate_sections(resume_text):
    required_sections = ['work experience', 'education', 'skills']
    found_sections = {section: section in resume_text.lower() for section in required_sections}
    return found_sections
