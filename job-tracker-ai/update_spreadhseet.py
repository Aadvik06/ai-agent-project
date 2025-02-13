import sqlite3

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("data/job_applications.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY,
            job_title TEXT,
            company TEXT,
            application_date TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_job_application(job_title, company, application_date, status="Pending"):
    conn = sqlite3.connect("data/job_applications.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (job_title, company, application_date, status)
        VALUES (?, ?, ?, ?)
    ''', (job_title, company, application_date, status))
    conn.commit()
    conn.close()

def fetch_all_applications():
    conn = sqlite3.connect("data/job_applications.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM applications')
    rows = cursor.fetchall()
    conn.close()
    return rows