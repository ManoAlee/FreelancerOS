
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-Agent: DATA RECORDER (AI Memory)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import sqlite3
import datetime
import json
import os

# Ensure data directory exists
DB_DIR = os.path.join(os.path.dirname(__file__), '../../data')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "agent_memory.db")

class JobRecorder:
    def __init__(self):
        self.db_path = DB_PATH
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        """Creates the tables if they don't exist with RICH METADATA support."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT,
                link TEXT,
                status TEXT, -- NEW, ANALYZED, APPLIED, REJECTED, ERROR
                confidence INTEGER,
                ai_analysis TEXT, -- JSON dump of the Brain's reasoning
                proposal_content TEXT, -- what we sent
                found_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        self.conn.commit()

    def job_exists(self, job_id):
        self.cursor.execute("SELECT 1 FROM jobs WHERE id = ?", (job_id,))
        return self.cursor.fetchone() is not None

    def add_job(self, job):
        """Adds a new job discovery."""
        if not self.job_exists(job['id']):
            self.cursor.execute('''
                INSERT INTO jobs (id, title, link, status, found_at, updated_at)
                VALUES (?, ?, ?, 'NEW', ?, ?)
            ''', (job['id'], job['title'], job['link'], datetime.datetime.now(), datetime.datetime.now()))
            self.conn.commit()
            return True
        return False

    def save_analysis(self, job_id, confidence, analysis_json):
        """Stores the specialized AI Analysis."""
        self.cursor.execute('''
            UPDATE jobs 
            SET status = 'ANALYZED', 
                confidence = ?, 
                ai_analysis = ?,
                updated_at = ?
            WHERE id = ?
        ''', (confidence, json.dumps(analysis_json), datetime.datetime.now(), job_id))
        self.conn.commit()

    def mark_applied(self, job_id, proposal_text):
        self.cursor.execute('''
            UPDATE jobs 
            SET status = 'APPLIED', 
                proposal_content = ?, 
                updated_at = ?
            WHERE id = ?
        ''', (proposal_text, datetime.datetime.now(), job_id))
        self.conn.commit()

    def mark_rejected(self, job_id, reason="Low Score"):
        self.cursor.execute('''
            UPDATE jobs 
            SET status = 'REJECTED',
                updated_at = ?
            WHERE id = ?
        ''', (datetime.datetime.now(), job_id))
        self.conn.commit()

    def get_stats(self):
        self.cursor.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
        return dict(self.cursor.fetchall())
