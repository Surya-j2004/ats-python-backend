from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def semantic_similarity(resume_text, job_desc):
    vectorizer = TfidfVectorizer().fit([resume_text, job_desc])
    vectors = vectorizer.transform([resume_text, job_desc])
    sim_score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return sim_score
