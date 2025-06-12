import re
import nltk

try:
    from nltk.corpus import stopwords
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
    from nltk.corpus import stopwords


STOPWORDS = set(stopwords.words('english'))

EDUCATION = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S',
    'ME', 'M.E', 'M.E.', 'MS', 'M.S',
    'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
    'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII',
    'PHD', 'PH.D', 'MBA', 'BBA', 'BCA', 'MCA',
    'BSC', 'MSc', 'B.COM', 'M.COM', 'BA', 'MA'
]

def extract_education(resume_text):
    lines = resume_text.split('\n')
    education = []

    for i, line in enumerate(lines):
        words = line.split()
        for word in words:
            word_clean = re.sub(r'[?|$|.|!|,]', r'', word)
            word_upper = word_clean.upper()

            if word_upper in EDUCATION and word_upper.lower() not in STOPWORDS:
                combined_line = line
                if i + 1 < len(lines):
                    combined_line += ' ' + lines[i + 1]

                year_match = re.search(r'(((20|19)\d{2}))', combined_line)
                year = year_match.group() if year_match else None
                education.append((word_upper, year))
    
    return education
