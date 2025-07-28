import os
import json
from pathlib import Path

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ["data", "uploads", "logs", "templates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def load_config():
    """Load configuration from environment variables"""
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "firecrawl_api_key": os.getenv("FIRECRAWL_API_KEY"),
        "tavily_api_key": os.getenv("TAVILY_API_KEY"),
        "serp_api_key": os.getenv("SERP_API_KEY")
    }
    return config

def load_json_file(file_path):
    """Load and return JSON data from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {file_path}")
        return {}

def save_json_file(data, file_path):
    """Save data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False

def load_skills_database():
    """Load skills database from JSON file or return default skills"""
    try:
        with open('data/skills_database.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default skills if file doesn't exist
        return get_default_skills()

def get_default_skills():
    """Return a comprehensive list of default skills"""
    return [
        # Programming Languages
        "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "PHP", "Go", "Rust", "Swift",
        "Kotlin", "TypeScript", "Scala", "R", "MATLAB", "Perl", "Shell Scripting", "PowerShell",
        
        # Web Technologies
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
        "Spring Boot", "ASP.NET", "Laravel", "Bootstrap", "jQuery", "SASS", "LESS",
        
        # Databases
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", "SQL Server", "DynamoDB",
        "Cassandra", "Neo4j", "Elasticsearch", "Firebase",
        
        # Cloud & DevOps
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "GitLab CI", "Terraform",
        "Ansible", "Chef", "Puppet", "Nagios", "Prometheus", "Grafana",
        
        # Data Science & ML
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas",
        "NumPy", "Matplotlib", "Seaborn", "Jupyter", "Apache Spark", "Hadoop", "Tableau", "Power BI",
        
        # Mobile Development
        "Android", "iOS", "React Native", "Flutter", "Xamarin", "Ionic",
        
        # Version Control & Tools
        "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Jira", "Confluence", "Slack", "Trello",
        
        # Soft Skills
        "Project Management", "Agile", "Scrum", "Leadership", "Communication", "Problem Solving",
        "Team Collaboration", "Time Management", "Critical Thinking", "Adaptability",
        
        # Other Technologies
        "REST API", "GraphQL", "Microservices", "Blockchain", "IoT", "Cybersecurity", "Linux",
        "Windows Server", "Networking", "System Administration"
    ]

def save_skills_database(skills):
    """Save skills database to JSON file"""
    try:
        with open('data/skills_database.json', 'w') as f:
            json.dump(skills, f, indent=2)
    except Exception as e:
        print(f"Failed to save skills database: {str(e)}")

def format_job_for_display(job):
    """Format job data for better display"""
    formatted_job = job.copy()
    
    # Truncate long descriptions
    if len(formatted_job.get('description', '')) > 200:
        formatted_job['description'] = formatted_job['description'][:200] + "..."
    
    # Ensure URL is valid
    if not formatted_job.get('url', '').startswith('http'):
        formatted_job['url'] = '#'
    
    # Format match score as percentage
    if 'match_score' in formatted_job:
        formatted_job['match_percentage'] = f"{formatted_job['match_score'] * 100:.1f}%"
    
    return formatted_job
