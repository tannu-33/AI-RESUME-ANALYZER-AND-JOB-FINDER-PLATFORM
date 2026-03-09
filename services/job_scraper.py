import requests
import os
API_KEY = os.getenv("RAPID_API_KEY")

def fetch_jobs(role, job_type):

    url = "https://jsearch.p.rapidapi.com/search"

    # Modify query based on selection
    if job_type == "Internships":
        query_text = f"{role} internship in India"
    else:
        query_text = f"{role} jobs in India"

    querystring = {
        "query": query_text,
        "page": "1",
        "num_pages": "1",
        "country": "in",
        "language": "en"
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print("API Error:", response.text)
        return []

    data = response.json()

    jobs = []

    for job in data.get("data", []):
        jobs.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city"),
            "salary": job.get("job_salary"),
            "link": job.get("job_apply_link")
        })

    return jobs