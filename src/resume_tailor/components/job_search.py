import os
import requests

def search_jobs_adzuna(profile: dict, num_results: int = 3, country: str = "ca"):
    """
    Search for jobs using the Adzuna API based on the user's profile.
    Args:
        profile (dict): Should contain at least 'job_title' and optionally 'location' and 'skills'.
        num_results (int): Number of job results to return.
        country (str): Country code for Adzuna API (e.g., 'ca' for Canada).
    Returns:
        List of job dicts with keys: title, company, summary, link.
    """
    APP_ID = os.getenv("ADZUNA_APP_ID")
    APP_KEY = os.getenv("ADZUNA_APP_KEY")
    if not APP_ID or not APP_KEY:
        raise ValueError("Missing ADZUNA_APP_ID or ADZUNA_APP_KEY in environment.")

    job_title = profile.get("job_title", "")
    location = profile.get("location", "Canada")
    #skills = profile.get("skills", [])
    #what = f"{job_title} {' '.join(skills)}"
    what = f"{job_title}"

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": what,
        "where": location,
        "results_per_page": num_results,
        "content-type": "application/json"
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    job_listings = []
    seen_descriptions = set()
    for job in data.get("results", []):
        description = job.get("description", "")
        if description in seen_descriptions:
            continue
        seen_descriptions.add(description)
        job_listings.append({
            "adref": job.get("adref", ""),
            "title": job.get("title", "N/A"),
            "company": job.get("company", {}).get("display_name", "N/A"),
            "summary": description,
            "link": job.get("redirect_url", "")
        })
    return job_listings