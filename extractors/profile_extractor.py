def extract_job_titles(text, job_titles_list):
    found_titles = [title for title in job_titles_list if title.lower() in text.lower()]
    return found_titles
