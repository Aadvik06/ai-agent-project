import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import streamlit as st
from datetime import datetime

class EmailService:
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_job_recommendations(self, user_name: str, user_email: str, 
                               job_matches: List[Dict], resume_data: Dict) -> bool:
        """Send job recommendations via email"""
        
        try:
            # Create email content
            subject = f"🎯 Your Personalized Job Recommendations - {len(job_matches)} Perfect Matches!"
            
            # Create HTML email body
            html_body = self._create_email_html(user_name, job_matches, resume_data)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = user_email
            
            # Add HTML part
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
            return False
    
    def _create_email_html(self, user_name: str, job_matches: List[Dict], resume_data: Dict) -> str:
        """Create HTML email content"""
        
        # Generate job cards HTML
        job_cards_html = ""
        for i, job in enumerate(job_matches, 1):
            match_percentage = int(job['match_score'] * 100)
            skills_match = ", ".join(job.get('skills_match', [])[:5])
            
            job_cards_html += f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin: 15px 0; background: #ffffff;">
                <h3 style="color: #2c3e50; margin: 0 0 10px 0;">#{i} {job['title']}</h3>
                <p style="color: #7f8c8d; margin: 5px 0;"><strong>Company:</strong> {job['company']}</p>
                <p style="color: #7f8c8d; margin: 5px 0;"><strong>Location:</strong> {job['location']}</p>
                <p style="color: #7f8c8d; margin: 5px 0;"><strong>Type:</strong> {job['job_type']}</p>
                <div style="background: #ecf0f1; padding: 10px; border-radius: 5px; margin: 10px 0;">
                    <p style="margin: 0; color: #2c3e50;"><strong>Match Score: {match_percentage}%</strong></p>
                    <p style="margin: 5px 0; color: #34495e; font-size: 14px;">Matching Skills: {skills_match}</p>
                </div>
                <a href="{job['url']}" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px;">Apply Now</a>
            </div>
            """
        
        # Complete HTML template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your Job Recommendations</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
            
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                <h1 style="margin: 0; font-size: 28px;">🎯 Your Perfect Job Matches</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Personalized recommendations powered by AI</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <h2 style="color: #2c3e50; margin-top: 0;">Hello {user_name}! 👋</h2>
                <p>Great news! Our AI has analyzed your resume and found <strong>{len(job_matches)} perfect job matches</strong> tailored to your skills and experience.</p>
                <p><strong>Your Skills:</strong> {", ".join(resume_data['skills'][:8])}</p>
                <p><strong>Experience Level:</strong> {resume_data['experience_level']}</p>
                <p><strong>Analysis Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">🚀 Top Job Recommendations</h2>
            
            {job_cards_html}
            
            <div style="background: #e8f5e8; border-left: 4px solid #27ae60; padding: 20px; margin: 30px 0; border-radius: 0 8px 8px 0;">
                <h3 style="color: #27ae60; margin-top: 0;">💡 Pro Tips for Success:</h3>
                <ul style="color: #2c3e50;">
                    <li>Tailor your resume for each application</li>
                    <li>Research the company culture and values</li>
                    <li>Prepare specific examples of your achievements</li>
                    <li>Follow up within a week of applying</li>
                    <li>Practice your interview skills regularly</li>
                </ul>
            </div>
            
            <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px; margin-top: 30px;">
                <p style="color: #7f8c8d; margin: 0;">Best of luck with your job search! 🍀</p>
                <p style="color: #7f8c8d; margin: 5px 0 0 0; font-size: 14px;">Generated by Job Finding AI Assistant</p>
            </div>
            
        </body>
        </html>
        """
        
        return html_template