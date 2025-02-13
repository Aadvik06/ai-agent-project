import requests
from bs4 import BeautifulSoup
import re

def scrape_urls(urls):
    """
    Scrapes a list of job posting URLs to extract job descriptions.

    Args:
        urls (list): List of job posting URLs.

    Returns:
        list: A list of dictionaries containing job descriptions or errors.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    scraped_data = []

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                scraped_data.append({"url": url, "error": "Could not access job posting"})
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            
            # Try extracting job description from multiple possible elements
            job_description = None
            for tag in ["div", "section", "article"]:
                job_description = soup.find(tag, class_=re.compile("description", re.IGNORECASE))
                if job_description:
                    break
            
            job_text = job_description.get_text().strip() if job_description else "No job description found"
            
            scraped_data.append({"url": url, "job_description": job_text})
        
        except Exception as e:
            scraped_data.append({"url": url, "error": str(e)})
    
    return scraped_data

# Example usage
if __name__ == "__main__":
    test_urls = [
        "https://example.com/job1",
        "https://example.com/job2"
    ]
    results = scrape_urls(test_urls)
    for result in results:
        print(result)

    
