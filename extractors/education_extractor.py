import re
import spacy
from nltk.corpus import stopwords

# Load spaCy model
nlp = spacy.load('en_core_web_sm')
STOPWORDS = set(stopwords.words('english'))

# Common degree keywords
EDUCATION = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S',
    'ME', 'M.E', 'M.E.', 'MS', 'M.S',
    'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
    'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII',
    'PHD', 'PH.D', 'MBA', 'BBA', 'BCA', 'MCA',
    'BSC', 'MSc', 'B.COM', 'M.COM', 'BA', 'MA'
]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)
    sentences = [sent.text.strip() for sent in nlp_text.sents]
    edu = {}
    for index, sent in enumerate(sentences):
        for word in sent.split():
            word_clean = re.sub(r'[?|$|.|!|,]', r'', word)
            if word_clean.upper() in EDUCATION and word_clean.lower() not in STOPWORDS:
                next_sent = sentences[index + 1] if index + 1 < len(sentences) else ''
                edu[word_clean] = sent + ' ' + next_sent
    education = []
    for key in edu.keys():
        year = re.search(r'(((20|19)(\d{2})))', edu[key])
        if year:
            education.append((key, year.group()))
        else:
            education.append((key, None))
    return education
