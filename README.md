# **AI Agent-Powered Job Application Tracker**

## **Overview**
The **AI Agent-Powered Job Application Tracker** is an automated system designed to help job seekers track and monitor their job applications efficiently. This project integrates **LangChain, OpenAI, Google Search APIs, and Gmail automation** to streamline the job search process. 

With the power of **web scraping, AI-driven classification, and automated email notifications**, the agent helps users:
- Find relevant job postings.
- Determine whether job applications are **open or closed** using AI.
- Store and update job application statuses in a structured spreadsheet.
- Receive **email alerts** about job status updates.

This project serves as a personal **AI job assistant**, enhancing productivity and ensuring users stay informed about their application progress in real time.

---
## **Features**

### 🔍 **Automated Job Search & Scraping**
- Uses **Google Search API (SerpAPI)** to find **relevant job postings** based on **job title and company**.
- Scrapes the top **2-3** job posting websites for additional job-related details.
- Extracts valuable context from job descriptions for AI processing.

### 🤖 **AI-Powered Job Status Classification**
- The scraped job information is passed to **OpenAI’s LLM (GPT model)**.
- The AI **analyzes the job details** and determines if the **job is open or closed**.
- This eliminates the need for manual checking and provides instant insights.

### 📊 **Automated Job Application Tracking**
- The agent **logs job title, company, and status (open/closed) into a structured spreadsheet**.
- Provides an easy-to-access database of all job applications.
- Keeps track of multiple applications without manual input.

### 📧 **Email Alerts & Notifications**
- Users receive **automated email updates** about job statuses.
- Ensures applicants are notified immediately when a job status changes.
- Helps users stay proactive in their job search without constantly checking postings.

---
## **Project Workflow**

1. **User Input** → User provides **job title** and **company name**.
2. **Web Search & Scraping** → The agent **searches Google**, finds relevant postings, and **extracts job details**.
3. **AI Processing** → The extracted job details are **passed to OpenAI**, which classifies whether the **job is open or closed**.
4. **Database Update** → The structured job data is **saved to a spreadsheet**.
5. **Email Notifications** → The user receives **email alerts** on job status updates.

---
## **Tech Stack**

| **Technology** | **Usage** |
|---------------|----------|
| **Python** | Core programming language |
| **LangChain** | AI agent framework for processing job data |
| **OpenAI API** | AI model for job status classification |
| **SerpAPI** | Web search tool to find job postings |
| **BeautifulSoup** | Web scraping to extract job details |
| **Google Sheets API** | Storing job application records |
| **SMTP (Gmail API)** | Sending automated job status notifications |

---
## **Installation & Setup**

### **Prerequisites**
Ensure you have **Python 3.8+** installed along with the required dependencies.

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/job-tracker-ai.git
cd job-tracker-ai
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**
Create a `.env` file in the root directory and add the following credentials:
```
SERPAPI_API_KEY=your_serpapi_key
OPENAI_API_KEY=your_openai_key
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_email_password
```

### **4️⃣ Run the Program**
```bash
python main.py
```

---
## **Project Structure**
```
job-tracker-ai/
│── main.py                    # Main entry point
│── find_relevant_websites.py   # Web search tool using SerpAPI
│── scrape_job_posting_info.py  # Scraper for job details
│── classify_job_status.py      # AI model for status classification
│── update_spreadsheet.py       # Updates Google Sheets
│── send_email_notifications.py # Gmail automation for alerts
│── requirements.txt            # Dependencies
│── .env                        # API keys and credentials
```

---
## **Usage Instructions**
1. **Run the program** and enter a job title and company name.
2. The agent will **search the web** and scrape job details.
3. AI will determine whether the job **is open or closed**.
4. The job details will be **logged in a spreadsheet**.
5. The user will receive an **email notification** with the job status.

---
## **Example Output**
### **User Input:**
```
Job Title: Software Engineer
Company: Google
```
### **System Processing:**
```
- Searching Google for job postings...
- Scraping job details from Google Careers...
- Job status: OPEN (determined by AI)
- Updating spreadsheet...
- Sending email notification...
```
### **Email Notification Sent:**
```
Subject: Job Application Status Update

Your application for Software Engineer at Google is still OPEN!
Check the job posting for more details.
```

---
## **Future Improvements**
✅ Expand support for LinkedIn & Indeed API integration.  
✅ Enhance AI model accuracy with more training data.  
✅ Implement a dashboard for real-time job tracking.  

---
## **Contributions**
Contributions are welcome! Feel free to submit pull requests or open issues.

📩 **Contact:** [Your Email] | 🌐 [Your LinkedIn/GitHub]

---
## **License**
This project is licensed under the MIT License. See `LICENSE` for details.

