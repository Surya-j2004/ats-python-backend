def extract_location(text):
    # Example: look for common locations or keywords
    locations = ['bangalore', 'mumbai', 'delhi', 'chennai', 'hyderabad', 'remote', 'india']
    text = text.lower()
    for loc in locations:
        if loc in text:
            return loc
    return None

def location_score(resume_text, job_location):
    resume_loc = extract_location(resume_text)
    job_loc = job_location.lower()
    if not job_loc:
        return 0.0
    if resume_loc is None:
        return 0.0
    if resume_loc == job_loc or resume_loc == 'remote' or job_loc == 'remote':
        return 1.0
    if resume_loc in job_loc or job_loc in resume_loc:
        return 0.5
    return 0.0
