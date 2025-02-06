import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"url": url, "error" : "could not access job posting"}
        
        soup = BeautifulSoup(response.text, "html.parser")
        job_description = soup.find('div', class_="job-description")

        if job_description:
            job_text = job_description.get_text().strip()
        else:
            job_text = "No job description found"

        return {
            "url": url,
            "job_description": job_text
        }
    
    except Exception as e:
        return {"url": url, "error": str(e)}
    
    
