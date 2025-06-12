def extract_soft_skills(text, soft_skills_list):
    return [skill for skill in soft_skills_list if skill.lower() in text.lower()]
