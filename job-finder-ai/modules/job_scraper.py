import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict
from urllib.parse import urlencode, quote_plus
import streamlit as st

class JobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_jobs(self, skills: List[str], location: str = "Remote", 
                   job_type: str = "Full-time", max_jobs: int = 50) -> List[Dict]:
        """Search for jobs across multiple platforms"""
        all_jobs = []
        
        # Create search query from skills
        query = " ".join(skills[:5])  # Use top 5 skills
        
        try:
            # Search Indeed
            indeed_jobs = self._search_indeed(query, location, max_jobs//2)
            all_jobs.extend(indeed_jobs)
            
            # Search SimplyHired (as backup)
            simplyhired_jobs = self._search_simplyhired(query, location, max_jobs//2)
            all_jobs.extend(simplyhired_jobs)
            
            # Remove duplicates based on title and company
            unique_jobs = self._remove_duplicates(all_jobs)
            
            st.info(f"Scraped {len(unique_jobs)} unique jobs from multiple sources")
            return unique_jobs[:max_jobs]
            
        except Exception as e:
            st.warning(f"Job scraping encountered issues: {str(e)}")
            # Return sample jobs as fallback
            return self._get_sample_jobs(skills, location)
    
    def _search_indeed(self, query: str, location: str, max_jobs: int) -> List[Dict]:
        """Search Indeed for jobs"""
        jobs = []
        
        try:
            # Build Indeed search URL
            params = {
                'q': query,
                'l': location,
                'sort': 'date',
                'limit': min(max_jobs, 50)
            }
            url = f"https://www.indeed.com/jobs?{urlencode(params)}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:max_jobs]:
                try:
                    # Extract job information
                    title_elem = card.find('h2', class_='jobTitle')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    company_elem = card.find('span', class_='companyName')
                    company = company_elem.get_text(strip=True) if company_elem else "N/A"
                    
                    location_elem = card.find('div', class_='companyLocation')
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    # Get job URL
                    link_elem = title_elem.find('a') if title_elem else None
                    job_url = f"https://www.indeed.com{link_elem['href']}" if link_elem and link_elem.get('href') else "#"
                    
                    # Extract description snippet
                    desc_elem = card.find('div', class_='summary')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': job_location,
                        'url': job_url,
                        'description': description,
                        'source': 'Indeed',
                        'job_type': 'Full-time',  # Default
                        'posted_date': 'Recently'
                    })
                    
                except Exception as e:
                    continue
            
            # Add delay to be respectful
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            st.warning(f"Indeed scraping failed: {str(e)}")
        
        return jobs
    
    def _search_simplyhired(self, query: str, location: str, max_jobs: int) -> List[Dict]:
        """Search SimplyHired for jobs (alternative source)"""
        jobs = []
        
        try:
            # Build SimplyHired URL
            params = {
                'q': query,
                'l': location,
                'job': max_jobs
            }
            url = f"https://www.simplyhired.com/search?{urlencode(params)}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings
            job_cards = soup.find_all('div', class_='SerpJob-jobCard')
            
            for card in job_cards[:max_jobs]:
                try:
                    title_elem = card.find('a', class_='SerpJob-titleLink')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    company_elem = card.find('span', class_='SerpJob-companyName')
                    company = company_elem.get_text(strip=True) if company_elem else "N/A"
                    
                    location_elem = card.find('span', class_='SerpJob-location')
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    job_url = title_elem['href'] if title_elem and title_elem.get('href') else "#"
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': job_location,
                        'url': job_url,
                        'description': "",
                        'source': 'SimplyHired',
                        'job_type': 'Full-time',
                        'posted_date': 'Recently'
                    })
                    
                except Exception as e:
                    continue
            
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            st.warning(f"SimplyHired scraping failed: {str(e)}")
        
        return jobs
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on title and company"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            identifier = f"{job['title'].lower()}_{job['company'].lower()}"
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _get_sample_jobs(self, skills: List[str], location: str) -> List[Dict]:
        """Return sample jobs when scraping fails"""
        sample_jobs = [
            {
                'title': f'{skills[0] if skills else "Software"} Developer',
                'company': 'Tech Solutions Inc',
                'location': location,
                'url': 'https://example.com/job1',
                'description': f'Looking for someone with {", ".join(skills[:3]) if skills else "programming"} skills',
                'source': 'Sample',
                'job_type': 'Full-time',
                'posted_date': 'Today'
            },
            {
                'title': f'Senior {skills[1] if len(skills) > 1 else "Software"} Engineer',
                'company': 'Innovation Corp',
                'location': location,
                'url': 'https://example.com/job2',
                'description': f'Expert level position requiring {", ".join(skills[:2]) if skills else "technical"} expertise',
                'source': 'Sample',
                'job_type': 'Full-time',
                'posted_date': '2 days ago'
            },
            {
                'title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'location': location,
                'url': 'https://example.com/job3',
                'description': 'Join our dynamic team and work with cutting-edge technologies',
                'source': 'Sample',
                'job_type': 'Full-time',
                'posted_date': '1 week ago'
            },
            {
                'title': f'{skills[0] if skills else "Data"} Analyst',
                'company': 'DataTech Solutions',
                'location': location,
                'url': 'https://example.com/job4',
                'description': 'Analyze complex datasets and provide insights',
                'source': 'Sample',
                'job_type': 'Contract',
                'posted_date': '3 days ago'
            },
            {
                'title': 'Product Manager',
                'company': 'Global Enterprises',
                'location': location,
                'url': 'https://example.com/job5',
                'description': 'Lead product development and strategy initiatives',
                'source': 'Sample',
                'job_type': 'Full-time',
                'posted_date': '5 days ago'
            }
        ]
        
        return sample_jobs
