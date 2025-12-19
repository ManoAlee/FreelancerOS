
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-Agent: THE HUNTER (Input System)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import feedparser
import time
import random

# Target Feeds (Simulated "Freelance Markets")
SOURCES = [
    "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-design-jobs.rss",
    # Add Upwork RSS here if user has specific feed
]

class Hunter:
    def __init__(self):
        self.seen_jobs = set()

    def scan(self):
        """Scans all sources for NEW jobs."""
        print("\n👁️  [HUNTER] Scanning for targets...")
        found_jobs = []
        
        for url in SOURCES:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]: # Check top 5
                    job_id = entry.link
                    if job_id not in self.seen_jobs:
                        self.seen_jobs.add(job_id)
                        job_data = {
                            "id": job_id,
                            "title": entry.title,
                            "summary": entry.summary[:500], # First 500 chars
                            "link": entry.link
                        }
                        found_jobs.append(job_data)
            except Exception as e:
                print(f"⚠️  [HUNTER] Error scanning {url}: {e}")
        
        if found_jobs:
            print(f"🎯 [HUNTER] Spotted {len(found_jobs)} new opportunities.")
        else:
            print("💤 [HUNTER] No new targets.")
            
        return found_jobs
