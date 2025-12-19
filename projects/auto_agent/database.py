
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-Agent: DATABASE LAYER (Persistence)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import sqlite3
import datetime

DB_PATH = "projects/auto_agent/agent_memory.db"

class JobDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        """Creates the tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT,
                link TEXT,
                status TEXT, -- NEW, APPLIED, REJECTED, ERROR
                confidence INTEGER,
                found_at TIMESTAMP
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
                INSERT INTO jobs (id, title, link, status, found_at)
                VALUES (?, ?, ?, 'NEW', ?)
            ''', (job['id'], job['title'], job['link'], datetime.datetime.now()))
            self.conn.commit()
            return True
        return False

    def mark_applied(self, job_id, confidence):
        self.cursor.execute('''
            UPDATE jobs SET status = 'APPLIED', confidence = ? WHERE id = ?
        ''', (confidence, job_id))
        self.conn.commit()

    def mark_rejected(self, job_id, reason="Low Score"):
        self.cursor.execute('''
            UPDATE jobs SET status = 'REJECTED' WHERE id = ?
        ''', (job_id,))
        self.conn.commit()

    def get_stats(self):
        self.cursor.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
        return dict(self.cursor.fetchall())
