from collections import Counter

def keyword_score(resume_text, job_keywords):
    resume_words = resume_text.lower().split()
    resume_counts = Counter(resume_words)
    job_keywords = [kw.lower() for kw in job_keywords]
    matched = [kw for kw in job_keywords if kw in resume_counts]
    coverage = len(matched) / len(set(job_keywords)) if job_keywords else 0
    density = sum(resume_counts[kw] for kw in job_keywords) / len(resume_words) if resume_words else 0
    return {
        'matched_keywords': matched,
        'coverage': coverage,
        'density': density
    }
