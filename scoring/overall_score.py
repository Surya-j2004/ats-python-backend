def calculate_ats_score(metrics):
    # Example weights (adjust as needed)
    weights = {
        'skills': 0.4,
        'semantic': 0.2,
        'sections': 0.1,
        'experience': 0.1,
        'education': 0.1,
        'job_title': 0.1,
        'location': 0.05,
        'soft_skills': 0.05,
        'formatting': 0.1
    }
    score = sum(metrics[key] * weights[key] for key in metrics)
    return round(score * 100, 2)
