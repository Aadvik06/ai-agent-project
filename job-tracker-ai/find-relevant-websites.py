import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

def search_job_posting(job_title, company, search_results=2):
    serpapi_key = os.getenv("SERP_API_KEY")
    if not serpapi_key:
        raise ValueError("SERP_API_KEY not found in environment variables")
    
    search_query = f"{job_title} {company} job application"

    search = GoogleSearch({
        "q": search_query,
        "api_key": serpapi_key,
        "num": search_results
    })

    results = search.get_dict().get("organic_results",[])
    job_urls = [result.get("link") for result in results if result.get("link")]
    return job_urls

if __name__ == "__main__":
    job_title = input("Enter job title: ")
    company = input("Enter company name: ")
    urls = search_job_posting(job_title, company)
    print("Top job URLs:", urls)