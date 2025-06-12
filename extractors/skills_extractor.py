import re
from typing import List, Set

def extract_skills(text: str, skill_list: List[str]) -> List[str]:
    """
    Extract skills from text using pattern matching
    
    Args:
        text: Input text to extract skills from
        skill_list: List of skills to search for
    
    Returns:
        List of found skills
    """
    if not text or not skill_list:
        return []
    
    found_skills = set()
    text_lower = text.lower()
    
    for skill in skill_list:
        skill_lower = skill.lower().strip()
        
        # Multiple matching strategies for better accuracy
        patterns = [
            # Exact word boundary match
            r'\b' + re.escape(skill_lower) + r'\b',
            # With optional 's' for plurals
            r'\b' + re.escape(skill_lower) + r's?\b',
            # Handle spaces and variations
            skill_lower.replace(' ', r'\s+'),
            # Handle dots in technology names (e.g., Node.js)
            re.escape(skill_lower).replace(r'\.', r'\.?'),
        ]
        
        for pattern in patterns:
            try:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    found_skills.add(skill)
                    break
            except re.error:
                # Fallback to simple string matching if regex fails
                if skill_lower in text_lower:
                    found_skills.add(skill)
                break
    
    return list(found_skills)
