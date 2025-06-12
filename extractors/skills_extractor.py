import spacy

nlp = spacy.load('en_core_web_sm')

def extract_skills(text, skill_list):
    doc = nlp(text)
    skills_found = [token.text for token in doc if token.text.lower() in skill_list]
    return set(skills_found)
