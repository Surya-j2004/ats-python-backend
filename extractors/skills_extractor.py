import re
from typing import List, Set

# Try to import and load spaCy, but don't fail if it's not available
try:
    import spacy
    try:
        nlp = spacy.load('en_core_web_sm')
        SPACY_AVAILABLE = True
        print("✅ spaCy model loaded successfully")
    except OSError:
        print("⚠️  spaCy model 'en_core_web_sm' not found, using fallback method")
        nlp = None
        SPACY_AVAILABLE = False
except ImportError:
    print("⚠️  spaCy not installed, using fallback method")
    nlp = None
    SPACY_AVAILABLE = False

def extract_skills(text: str, skill_list: List[str]) -> List[str]:
    """
    Extract skills from text using spaCy if available, otherwise regex
    
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
    
    if SPACY_AVAILABLE and nlp:
        # Use spaCy for better text processing
        try:
            doc = nlp(text)
            tokens = [token.text.lower() for token in doc]
            lemmas = [token.lemma_.lower() for token in doc]
            
            for skill in skill_list:
                skill_lower = skill.lower().strip()
                
                # Check exact match in original text
                if skill_lower in text_lower:
                    found_skills.add(skill)
                # Check in tokens
                elif skill_lower in tokens:
                    found_skills.add(skill)
                # Check in lemmas for word variations
                elif skill_lower in lemmas:
                    found_skills.add(skill)
                # Check for partial matches in compound tokens
                else:
                    for token in tokens:
                        if skill_lower in token or token in skill_lower:
                            found_skills.add(skill)
                            break
        except Exception as e:
            print(f"⚠️  spaCy processing failed: {e}, falling back to regex")
            SPACY_AVAILABLE = False
    
    if not SPACY_AVAILABLE:
        # Fallback to regex-based extraction
        for skill in skill_list:
            skill_lower = skill.lower().strip()
            
            # Multiple matching strategies
            patterns = [
                r'\b' + re.escape(skill_lower) + r'\b',  # Exact word match
                r'\b' + re.escape(skill_lower) + r's?\b',  # With optional 's'
                skill_lower.replace(' ', r'\s+'),  # Handle multiple spaces
                re.escape(skill_lower).replace(r'\.', r'\.?'),  # Handle dots
            ]
            
            for pattern in patterns:
                try:
                    if re.search(pattern, text_lower, re.IGNORECASE):
                        found_skills.add(skill)
                        break
                except re.error:
                    # Ultimate fallback to simple string matching
                    if skill_lower in text_lower:
                        found_skills.add(skill)
                    break
    
    return list(found_skills)

def extract_skills_with_context(text: str, skill_list: List[str]) -> dict:
    """
    Extract skills with surrounding context
    """
    if not SPACY_AVAILABLE:
        return {skill: [] for skill in extract_skills(text, skill_list)}
    
    results = {}
    doc = nlp(text)
    
    for skill in skill_list:
        skill_lower = skill.lower()
        contexts = []
        
        for sent in doc.sents:
            if skill_lower in sent.text.lower():
                contexts.append(sent.text.strip())
        
        if contexts:
            results[skill] = contexts
    
    return results

# Include the same helper functions from the previous version
def get_common_tech_skills():
    """Return common technical skills by category"""
    return {
        "Programming Languages": [
            "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", 
            "Go", "Rust", "Swift", "Kotlin", "TypeScript", "Scala", "R"
        ],
        "Web Technologies": [
            "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", 
            "Express", "Django", "Flask", "Spring", "Laravel", "ASP.NET"
        ],
        "Databases": [
            "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle",
            "SQL Server", "MariaDB", "Cassandra", "DynamoDB"
        ],
        "Cloud & DevOps": [
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", 
            "Git", "Linux", "CI/CD", "Terraform", "Ansible"
        ]
    }

def extract_technical_skills_auto(text: str) -> List[str]:
    """Automatically extract technical skills"""
    skill_categories = get_common_tech_skills()
    all_skills = []
    
    for skills in skill_categories.values():
        all_skills.extend(skills)
    
    return extract_skills(text, all_skills)
