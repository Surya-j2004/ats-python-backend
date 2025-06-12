import re

def extract_years_of_experience(text):
    # Simple regex to find years of experience
    match = re.findall(r'(\d+)\s+years?', text.lower())
    return max(map(int, match)) if match else 0
