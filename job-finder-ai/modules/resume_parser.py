import PyPDF2
import docx
import re
from typing import Dict, List
import streamlit as st
from .utils import load_skills_database

class ResumeParser:
    def __init__(self):
        self.skills_db = load_skills_database()
    
    def parse_resume(self, uploaded_file):
        """Parse resume and extract relevant information"""
        
        # Extract text from file
        if uploaded_file.type == "application/pdf":
            text = self._extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = self._extract_text_from_docx(uploaded_file)
        else:
            raise ValueError("Unsupported file format")
        
        # Parse the extracted text
        resume_data = {
            'raw_text': text,
            'skills': self._extract_skills(text),
            'experience_level': self._determine_experience_level(text),
            'education': self._extract_education(text),
            'job_titles': self._extract_job_titles(text),
            'companies': self._extract_companies(text),
            'contact_info': self._extract_contact_info(text)
        }
        
        return resume_data
    
    def _extract_text_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    def _extract_text_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        found_skills = []
        text_lower = text.lower()
        
        # Check against skills database
        for skill in self.skills_db:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def _determine_experience_level(self, text: str) -> str:
        """Determine experience level based on resume content"""
        text_lower = text.lower()
        
        # Count years of experience mentioned
        years_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        years_matches = re.findall(years_pattern, text_lower)
        
        if years_matches:
            max_years = max(int(year) for year in years_matches)
            if max_years >= 8:
                return "Senior Level"
            elif max_years >= 3:
                return "Mid Level"
            else:
                return "Entry Level"
        
        # Check for senior indicators
        senior_indicators = ['senior', 'lead', 'principal', 'architect', 'director', 'manager']
        if any(indicator in text_lower for indicator in senior_indicators):
            return "Senior Level"
        
        # Check for entry-level indicators
        entry_indicators = ['intern', 'graduate', 'junior', 'entry', 'trainee']
        if any(indicator in text_lower for indicator in entry_indicators):
            return "Entry Level"
        
        return "Mid Level"  # Default
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        education_patterns = [
            r'(bachelor|master|phd|doctorate|associate).*?(?:degree|of)',
            r'(b\.?[ase]\.?|m\.?[ase]\.?|ph\.?d\.?)',
            r'(university|college|institute)\s+of\s+\w+'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education.extend(matches)
        
        return list(set(education))
    
    def _extract_job_titles(self, text: str) -> List[str]:
        """Extract job titles from resume"""
        # This is a simplified extraction - in practice, you'd use more sophisticated NLP
        job_title_patterns = [
            r'(software engineer|developer|programmer|analyst|manager|director|consultant)',
            r'(data scientist|machine learning|ai engineer|devops|product manager)',
        ]
        
        titles = []
        for pattern in job_title_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            titles.extend(matches)
        
        return list(set(titles))
    
    def _extract_companies(self, text: str) -> List[str]:
        """Extract company names (simplified)"""
        # This would typically use NER or company databases
        companies = []
        company_indicators = ['inc', 'llc', 'corp', 'ltd', 'company', 'technologies']
        
        lines = text.split('\n')
        for line in lines:
            if any(indicator in line.lower() for indicator in company_indicators):
                # Simple extraction - in practice, use NER
                companies.append(line.strip()[:50])  # Limit length
        
        return companies[:5]  # Return top 5
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        contact = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, text)
        if email_matches:
            contact['email'] = email_matches[0]
        
        # Phone pattern
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phone_matches = re.findall(phone_pattern, text)
        if phone_matches:
            contact['phone'] = ''.join(phone_matches[0])
        
        return contact
