from typing import Dict, List
import re
from collections import Counter
import streamlit as st

class MatchingEngine:
    def __init__(self):
        self.skill_weights = {
            'exact_match': 1.0,
            'partial_match': 0.7,
            'related_match': 0.5
        }
    
    def find_best_matches(self, resume_data: Dict, jobs: List[Dict], top_k: int = 5) -> List[Dict]:
        """Find the best job matches for the resume"""
        
        scored_jobs = []
        user_skills = [skill.lower() for skill in resume_data['skills']]
        user_experience = resume_data['experience_level']
        
        for job in jobs:
            score = self._calculate_match_score(job, user_skills, user_experience)
            job_with_score = job.copy()
            job_with_score['match_score'] = score
            job_with_score['skills_match'] = self._find_matching_skills(job, user_skills)
            scored_jobs.append(job_with_score)
        
        # Sort by match score and return top k
        scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        return scored_jobs[:top_k]
    
    def _calculate_match_score(self, job: Dict, user_skills: List[str], user_experience: str) -> float:
        """Calculate match score for a job"""
        total_score = 0.0
        
        # Skills matching (70% weight)
        skills_score = self._calculate_skills_score(job, user_skills)
        total_score += skills_score * 0.7
        
        # Experience level matching (20% weight)
        experience_score = self._calculate_experience_score(job, user_experience)
        total_score += experience_score * 0.2
        
        # Job title relevance (10% weight)
        title_score = self._calculate_title_score(job, user_skills)
        total_score += title_score * 0.1
        
        return min(total_score, 1.0)  # Cap at 1.0
    
    def _calculate_skills_score(self, job: Dict, user_skills: List[str]) -> float:
        """Calculate skills matching score"""
        if not user_skills:
            return 0.0
        
        job_text = f"{job['title']} {job['description']}".lower()
        
        matched_skills = 0
        total_user_skills = len(user_skills)
        
        for skill in user_skills:
            if skill in job_text:
                matched_skills += 1
            elif any(word in job_text for word in skill.split()):
                matched_skills += 0.7  # Partial match
        
        return min(matched_skills / total_user_skills, 1.0)
    
    def _calculate_experience_score(self, job: Dict, user_experience: str) -> float:
        """Calculate experience level matching score"""
        job_text = f"{job['title']} {job['description']}".lower()
        
        experience_mapping = {
            'Entry Level': ['entry', 'junior', 'graduate', 'intern', 'trainee', 'associate'],
            'Mid Level': ['mid', 'intermediate', 'experienced', 'professional'],
            'Senior Level': ['senior', 'lead', 'principal', 'architect', 'manager', 'director']
        }
        
        user_keywords = experience_mapping.get(user_experience, [])
        
        # Check for exact experience level matches
        for keyword in user_keywords:
            if keyword in job_text:
                return 1.0
        
        # Check for years of experience
        years_pattern = r'(\d+)\s*(?:years?|yrs?)'
        years_matches = re.findall(years_pattern, job_text)
        
        if years_matches:
            required_years = max(int(year) for year in years_matches)
            
            if user_experience == 'Entry Level' and required_years <= 2:
                return 0.9
            elif user_experience == 'Mid Level' and 3 <= required_years <= 7:
                return 0.9
            elif user_experience == 'Senior Level' and required_years >= 5:
                return 0.9
        
        return 0.5  # Default neutral score
    
    def _calculate_title_score(self, job: Dict, user_skills: List[str]) -> float:
        """Calculate job title relevance score"""
        job_title = job['title'].lower()
        
        # Check if any user skills appear in job title
        title_words = job_title.split()
        skill_matches = 0
        
        for skill in user_skills:
            skill_words = skill.lower().split()
            if any(word in title_words for word in skill_words):
                skill_matches += 1
        
        if not user_skills:
            return 0.5
        
        return min(skill_matches / len(user_skills), 1.0)
    
    def _find_matching_skills(self, job: Dict, user_skills: List[str]) -> List[str]:
        """Find which user skills match the job requirements"""
        job_text = f"{job['title']} {job['description']}".lower()
        matching_skills = []
        
        for skill in user_skills:
            if skill in job_text:
                matching_skills.append(skill.title())
            elif any(word in job_text for word in skill.split()):
                matching_skills.append(skill.title())
        
        return matching_skills