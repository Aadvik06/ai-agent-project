import os
import time
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

def search_job_posting(job_title, company, search_results=2, max_retries=3):
    """
    Searches for job postings using SerpAPI and returns a list of relevant URLs.

    Args:
        job_title (str): The job title to search for.
        company (str): The company associated with the job.
        search_results (int): Number of job postings to retrieve (default: 2).
        max_retries (int): Number of retries in case of request failure (default: 3).

    Returns:
        list: A list of job posting URLs.
    """
    serpapi_key = os.getenv("SERP_API_KEY")  # Ensure this matches your .env file
    if not serpapi_key:
        raise ValueError("SERP_API_KEY not found in environment variables")

    search_query = f"{job_title} {company} job application"

    for attempt in range(max_retries):
        try:
            search = GoogleSearch({
                "q": search_query,
                "api_key": serpapi_key,
                "num": search_results
            })

            results = search.get_dict().get("organic_results", [])
            job_urls = [result.get("link") for result in results if result.get("link")]

            if not job_urls:
                print("No job postings found. Try a different search query.")
            return job_urls[:search_results]  # Explicitly limit the number of URLs returned

        except Exception as e:
            print(f"Attempt {attempt + 1}: Error fetching job postings - {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                print("Max retries reached. Exiting search.")
                return []

if __name__ == "__main__":
    job_title = input("Enter job title: ")
    company = input("Enter company name: ")
    urls = search_job_posting(job_title, company)

    if urls:
        print("Top job URLs:", urls)
    else:
        print("No job postings found.")
