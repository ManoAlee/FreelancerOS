
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-Agent: THE BRAIN (Logic Core)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import sys
import os
import random

# Import FreelancerOS Capability
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'FreelancerOS'))
from freelanceros.modules import business_math, text_data, system_files, media_web

class Brain:
    def __init__(self):
        self.skills = {
            "python": ["Automating Scripts", "Data Processing", "Scraping"],
            "pdf": ["PDF Merging", "Document Conversion"],
            "excel": ["Spreadsheet Analysis", "CSV Conversion"],
            "web": ["Web Scraping", "Automation"],
            "image": ["Resize", "Optimization"],
            "design": ["Landing Page", "UI/UX"]
        }

    def analyze(self, job):
        """
        Decides if the job is doable.
        Returns: (confidence_score, proposed_action)
        """
        print(f"🧠 [BRAIN] Analyzing: '{job['title']}'")
        
        text = (job['title'] + " " + job['summary']).lower()
        
        # 1. Keyword Matching (Simulated AI)
        matched_skills = []
        for keyword, capabilities in self.skills.items():
            if keyword in text:
                matched_skills.extend(capabilities)
        
        # 2. Decision Logic
        if not matched_skills:
            print("❌ [BRAIN] verdict: SKIP (No skills match)")
            return None
        
        confidence = min(len(matched_skills) * 20, 99) # Cap at 99%
        action_plan = f"Execute: {', '.join(set(matched_skills))}"
        
        print(f"✅ [BRAIN] verdict: ACCEPT (Confidence: {confidence}%)")
        print(f"   PLEASED TO MEET YOU. I AM THE PERFECT FIT.")
        
        return {
            "job": job,
            "confidence": confidence,
            "plan": action_plan,
            "skills_used": list(set(matched_skills))
        }

    def execute_work(self, task):
        """
        Simulates doing the actual work using FreelancerOS tools.
        """
        print(f"⚙️  [BRAIN] Executing Plan: {task['plan']}...")
        
        # Mocking complex work using Simple Tools
        if "PDF" in task['plan']:
            # Example: call system_files tool
            res = system_files.count_files(".")
            return f"Processed PDF pipeline. Files checked: {res}"
            
        return "Task Completed Successfully via FreelancerOS Core."
