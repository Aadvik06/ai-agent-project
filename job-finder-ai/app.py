import streamlit as st
import pandas as pd
from datetime import datetime
import os
import sys
import json
from pathlib import Path

# Mock modules for demo purposes
class MockResumeParser:
    def parse_resume(self, uploaded_file):
        """Mock resume parsing for demo"""
        return {
            "skills": ["Python", "JavaScript", "React", "SQL", "Git"],
            "experience_level": "Mid Level",
            "education": "Bachelor's in Computer Science",
            "contact_info": {"email": "demo@example.com"},
            "raw_content": "Mock resume content"
        }

class MockJobScraper:
    def search_jobs(self, skills, location="Remote", job_type="Full-time"):
        """Mock job search for demo"""
        mock_jobs = [
            {
                "title": "Senior Python Developer",
                "company": "TechCorp Inc.",
                "location": location,
                "job_type": job_type,
                "url": "https://example.com/job1",
                "description": "We're looking for a senior Python developer with experience in Django and React.",
                "skills_required": ["Python", "Django", "React", "SQL"],
                "salary_range": "$120,000 - $150,000",
                "posted_date": "2024-02-14",
                "match_score": 0.85
            },
            {
                "title": "Data Scientist",
                "company": "DataFlow Analytics",
                "location": location,
                "job_type": job_type,
                "url": "https://example.com/job2",
                "description": "Join our data science team to build machine learning models.",
                "skills_required": ["Python", "Machine Learning", "Pandas", "NumPy"],
                "salary_range": "$130,000 - $160,000",
                "posted_date": "2024-02-13",
                "match_score": 0.75
            },
            {
                "title": "Full Stack Developer",
                "company": "StartupXYZ",
                "location": location,
                "job_type": job_type,
                "url": "https://example.com/job3",
                "description": "Build scalable web applications using modern technologies.",
                "skills_required": ["JavaScript", "React", "Node.js", "MongoDB"],
                "salary_range": "$100,000 - $130,000",
                "posted_date": "2024-02-12",
                "match_score": 0.65
            }
        ]
        return mock_jobs

class MockMatchingEngine:
    def find_best_matches(self, resume_data, jobs, top_k=5):
        """Mock job matching for demo"""
        # Add match scores and skills match to jobs
        for job in jobs:
            matching_skills = [skill for skill in resume_data['skills'] if skill in job.get('skills_required', [])]
            job['skills_match'] = matching_skills
            job['match_score'] = len(matching_skills) / max(len(job.get('skills_required', [])), 1)
        
        # Sort by match score and return top matches
        sorted_jobs = sorted(jobs, key=lambda x: x['match_score'], reverse=True)
        return sorted_jobs[:top_k]

class MockEmailService:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_job_recommendations(self, user_name, user_email, top_matches, resume_data):
        """Mock email sending for demo"""
        # In a real implementation, this would send actual emails
        return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ["data", "uploads", "logs", "templates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

# Try to import real modules, fall back to mocks
try:
    from modules.resume_parser import ResumeParser
    from modules.job_scraper import JobScraper
    from modules.matching_engine import MatchingEngine
    from modules.email_service import EmailService
    from modules.utils import create_directories, load_config
except ImportError:
    # Use mock classes if modules are not available
    ResumeParser = MockResumeParser
    JobScraper = MockJobScraper
    MatchingEngine = MockMatchingEngine
    EmailService = MockEmailService
    load_config = lambda: {}

# Page configuration
st.set_page_config(
    page_title="Job Finding AI Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processed_resume' not in st.session_state:
    st.session_state.processed_resume = None
if 'job_matches' not in st.session_state:
    st.session_state.job_matches = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

def main():
    st.title("🔍 Job Finding AI Assistant")
    st.markdown("### Find Your Perfect Job Match with AI")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Email configuration
        st.subheader("Email Settings")
        sender_email = st.text_input("Your Email", placeholder="your.email@gmail.com")
        sender_password = st.text_input("App Password", type="password", 
                                      help="Use app-specific password for Gmail")
        
        # Job search preferences
        st.subheader("Job Preferences")
        location = st.text_input("Preferred Location", value="Remote")
        job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Internship"])
        experience_level = st.selectbox("Experience Level", 
                                      ["Entry Level", "Mid Level", "Senior Level", "Executive"])
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📄 Upload Your Resume")
        
        # User information form
        with st.form("user_info_form"):
            user_name = st.text_input("Full Name", placeholder="John Doe")
            user_email = st.text_input("Email Address", placeholder="john.doe@email.com")
            
            # Resume upload
            uploaded_file = st.file_uploader(
                "Upload Resume (PDF or DOCX)", 
                type=['pdf', 'docx'],
                help="Upload your resume in PDF or Word format"
            )
            
            submit_button = st.form_submit_button("🚀 Find My Dream Jobs!")
        
        # Process the form submission
        if submit_button and uploaded_file and user_name and user_email:
            if not sender_email or not sender_password:
                st.error("Please configure your email settings in the sidebar!")
                return
            
            process_job_search(uploaded_file, user_name, user_email, sender_email, 
                             sender_password, location, job_type, experience_level)
    
    with col2:
        st.header("📊 Process Status")
        display_status_panel()
        
        if st.session_state.job_matches:
            st.header("🎯 Top Job Matches")
            display_job_matches()

def process_job_search(uploaded_file, user_name, user_email, sender_email, 
                      sender_password, location, job_type, experience_level):
    """Process the entire job search pipeline"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Parse Resume
        status_text.text("📄 Analyzing your resume...")
        progress_bar.progress(20)
        
        resume_parser = ResumeParser()
        resume_data = resume_parser.parse_resume(uploaded_file)
        st.session_state.processed_resume = resume_data
        
        st.success(f"✅ Resume parsed successfully! Found {len(resume_data['skills'])} skills.")
        
        # Step 2: Search for Jobs
        status_text.text("🔍 Searching for relevant jobs...")
        progress_bar.progress(40)
        
        job_scraper = JobScraper()
        jobs = job_scraper.search_jobs(resume_data['skills'], location, job_type)
        
        st.success(f"✅ Found {len(jobs)} potential job opportunities!")
        
        # Step 3: Match and Rank Jobs
        status_text.text("🎯 Matching jobs to your profile...")
        progress_bar.progress(60)
        
        matching_engine = MatchingEngine()
        top_matches = matching_engine.find_best_matches(resume_data, jobs, top_k=5)
        st.session_state.job_matches = top_matches
        
        # Step 4: Send Email
        status_text.text("📧 Sending personalized job recommendations...")
        progress_bar.progress(80)
        
        email_service = EmailService(sender_email, sender_password)
        email_sent = email_service.send_job_recommendations(
            user_name, user_email, top_matches, resume_data
        )
        
        progress_bar.progress(100)
        
        if email_sent:
            st.success("🎉 Success! Your personalized job recommendations have been sent to your email!")
            status_text.text("✅ Process completed successfully!")
        else:
            st.warning("⚠️ Jobs found but email sending failed. Check your email configuration.")
        
        st.session_state.processing_complete = True
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        status_text.text("❌ Process failed!")

def display_status_panel():
    """Display the current processing status"""
    if st.session_state.processed_resume:
        st.success("✅ Resume Processed")
        with st.expander("Resume Summary"):
            resume_data = st.session_state.processed_resume
            st.write(f"**Skills Found:** {', '.join(resume_data['skills'][:10])}")
            st.write(f"**Experience Level:** {resume_data['experience_level']}")
            st.write(f"**Education:** {resume_data['education']}")
    
    if st.session_state.job_matches:
        st.success("✅ Job Matches Found")
        st.metric("Top Matches", len(st.session_state.job_matches))
    
    if st.session_state.processing_complete:
        st.success("✅ Email Sent Successfully")

def display_job_matches():
    """Display the top job matches"""
    if not st.session_state.job_matches:
        return
    
    for i, job in enumerate(st.session_state.job_matches[:3], 1):
        with st.expander(f"Job {i}: {job['title']} at {job['company']}"):
            st.write(f"**Match Score:** {job.get('match_score', 0):.1%}")
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Type:** {job['job_type']}")
            st.write(f"**Link:** [Apply Here]({job['url']})")
            
            if job.get('skills_match'):
                st.write(f"**Matching Skills:** {', '.join(job['skills_match'][:5])}")

if __name__ == "__main__":
    create_directories()
    main()