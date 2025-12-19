import os
import time
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI

# Load Config
try:
    from FreelancerOS.config import CONFIG
except ImportError:
    CONFIG = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"), 
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"), 
        "HEADLESS": False
    }

# --- MEMORY SYSTEM ---
class Memory:
    def __init__(self, filename="mission_history.json"):
        self.filename = filename
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return {"applied_jobs": [], "blacklist": []}
        return {"applied_jobs": [], "blacklist": []}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.history, f, indent=4)

    def add_applied(self, url, title):
        if url not in [j['url'] for j in self.history['applied_jobs']]:
            self.history['applied_jobs'].append({
                "url": url,
                "title": title,
                "timestamp": time.time()
            })
            self.save()

    def is_processed(self, url):
        for job in self.history['applied_jobs']:
            if job['url'] == url:
                return True
        return False

# --- HEURISTIC BRAIN (FALLBACK) ---
class HeuristicBrain:
    """
    EMERGENCY BACKUP BRAIN.
    Uses regex and logic when AI APIs fail (Quota/Error).
    """
    @staticmethod
    def extract_jobs_from_text(text):
        print("   🧠 Cortex: Switching to Heuristic Mode (Regex)...")
        jobs = []
        lines = text.split('\n')
        
        # Keywords to look for
        keywords = ["python", "scraping", "automation", "bot", "script", "selenium", "excel"]
        
        for i, line in enumerate(lines):
            # Simple heuristic: Job titles usually > 10 chars, < 100 chars
            if len(line) > 10 and len(line) < 100:
                # Check if line contains relevant keywords
                if any(k in line.lower() for k in keywords):
                    # Check next few lines for price/budget
                    context = " ".join(lines[i:i+5])
                    if "$" in context or "USD" in context or "EUR" in context or "Fixed" in context or "Hourly" in context:
                        # Found a potential job
                        budget_match = re.search(r'\$\d+(?:-\$\d+)?', context)
                        budget = budget_match.group(0) if budget_match else "Unknown"
                        jobs.append({"title": line.strip(), "budget": budget})
        
        # Dedupe by title
        unique_jobs = {v['title']:v for v in jobs}.values()
        return list(unique_jobs)[:10] # Return top 10 matches

    @staticmethod
    def generate_bid(title):
        return f"I am an expert Python developer with extensive experience in automation and web scraping. I can deliver '{title}' efficiently using robust scripts. Ready to start immediately."

class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-flash-latest"]
        self.current_model_idx = 0
        self.headers = {"Content-Type": "application/json"}

    def _get_url(self):
        model = self.models[self.current_model_idx]
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

    def generate(self, prompt):
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        max_retries = len(self.models) + 1
        for attempt in range(max_retries):
            url = self._get_url()
            try:
                response = requests.post(url, headers=self.headers, json=data)
                if response.status_code == 200:
                    try:
                        return response.json()['candidates'][0]['content']['parts'][0]['text']
                    except: return None
                elif response.status_code == 429:
                    print(f"   ⚠️ Quota Exceeded on {self.models[self.current_model_idx]}. Switching...")
                    self.current_model_idx = (self.current_model_idx + 1) % len(self.models)
                    time.sleep(2)
                    continue
                else:
                    return None
            except: return None
        print("   ❌ All Gemini models exhausted.")
        return None

class FreelancerAgent:
    def __init__(self):
        self.openai_key = CONFIG.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.google_key = CONFIG.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = None
        self.gemini = None
        self.memory = Memory()
        
        if self.google_key:
            self.gemini = GeminiClient(self.google_key)
            print("   🧠 Cortex: Google Gemini (REST) Connected")

        if not self.gemini and self.openai_key:
            try:
                self.client = OpenAI(api_key=self.openai_key)
                print("   🧠 Cortex: OpenAI GPT-4o Connected")
            except: pass
        
        self.driver = self._setup_driver()
        self.persona = "YOU ARE AN ELITE FREELANCER AGENT. SKILLS: Python, Selenium, Automation. GOAL: Find jobs."

    def _setup_driver(self):
        options = Options()
        if CONFIG.get("HEADLESS", False):
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return webdriver.Chrome(options=options)

    def think(self, context, prompt):
        full_prompt = f"SYSTEM_PERSONA:\n{self.persona}\n\nCONTEXT:\n{context}\n\nTASK:\n{prompt}\n\nOUTPUT:\nJust the raw answer."
        if self.gemini:
            answer = self.gemini.generate(full_prompt)
            if answer: return answer.strip()
        if self.client:
            try:
                response = self.client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": full_prompt}])
                return response.choices[0].message.content.strip()
            except: pass
        return None

    def login(self, username, password):
        driver = self.driver
        print("\n🔑 Initiating AI-Login...")
        driver.get("https://www.freelancer.com/login")
        time.sleep(3)
        if "login" not in driver.current_url:
            print("   ✅ Already Logged In.")
            return True
        try:
            user_field = driver.find_element(By.CSS_SELECTOR, "input[name='user'], input[type='email']")
            user_field.clear()
            user_field.send_keys(username)
            time.sleep(1)
            pass_field = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']")
            pass_field.clear()
            pass_field.send_keys(password)
            time.sleep(1)
            pass_field.send_keys(Keys.RETURN)
            print("   ⏳ Credentials sent...")
            time.sleep(5)
            return True
        except Exception as e:
            print(f"   ❌ Login Failed: {e}")
            return False

    def scan_page_for_jobs(self):
        print("   👀 Reading page content...")
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            clean_text = body_text.replace("\n", " ")[:12000]
            
            prompt = """
            Analyze the text and extract job listings.
            CRITERIA:
            1. FILTER: Keep ONLY jobs strictly related to: Python, Web Scraping, Automation, Bots, Scripting, Excel VBA.
            2. EXCLUDE: Video editing, Design, Translation, Writing, Marketing.
            3. FORMAT: Return a valid JSON list: [{"title": "Job Title", "budget": "$XX"}].
            If no relevant jobs are found, return [].
            """
            
            print("   🧠 Analyzing & Filtering with AI...")
            response = self.think(clean_text, prompt)
            
            if not response:
                # FALLBACK TO HEURISTIC
                print("   ⚠️ AI Failed/Quota Exceeded. Switching to Heuristic Brain.")
                return HeuristicBrain.extract_jobs_from_text(self.driver.find_element(By.TAG_NAME, "body").text)
                
            if "```json" in response: response = response.split("```json")[1].split("```")[0]
            elif "```" in response: response = response.replace("```", "")
            return json.loads(response)
        except Exception as e:
            print(f"   ⚠️ Analysis Error: {e}")
            # FALLBACK TO HEURISTIC ON ERROR
            return HeuristicBrain.extract_jobs_from_text(self.driver.find_element(By.TAG_NAME, "body").text)

    def apply_to_job(self, job, job_url):
        print(f"      🤖 Analyzing Job Page: {self.driver.title}")
        
        bid_prompt = f"Write a professional, concise (2-3 sentences) bid for: {job['title']}. Emphasize Python, Selenium, and Automation skills."
        bid = self.think("I am an expert Python Automator.", bid_prompt)
        
        if not bid:
            print("      ⚠️ AI Bid Gen Failed. Using Template.")
            bid = HeuristicBrain.generate_bid(job['title'])

        print(f"      ✍️  Bid Prepared: \"{bid[:60]}...\"")
        
        try:
            print("      ⏳ Waiting for proposal form...")
            desc_box = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#description, textarea[name='description'], textarea[placeholder*='proposal'], textarea.proposal-description"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", desc_box)
            time.sleep(1)
            desc_box.clear()
            desc_box.send_keys(bid)
            time.sleep(1)
            
            print("      👆 Looking for Place Bid button...")
            place_btn = self.driver.find_element(By.CSS_SELECTOR, "button#place-bid, button[data-id='place-bid-btn'], button.btn-primary, button.btn-success")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", place_btn)
            time.sleep(1)
            
            place_btn.click()
            print("      🚀 BID SUBMITTED SUCCESSFULLY!")
            self.memory.add_applied(job_url, job['title'])
            
        except Exception as e:
            print(f"      ⚠️ Form interaction failed: {e}")

    def run_mission(self, mission_desc):
        print(f"\n🤖 MISSION START")
        user = CONFIG.get('FREELANCER_USER')
        pwd = CONFIG.get('FREELANCER_PASS')
        if user and "hotmail" in user: self.login(user, pwd)
        
        print(f"\n🔎 Searching for Targets...")
        self.driver.get("https://www.freelancer.com/jobs/python-automation/")
        time.sleep(5)
        
        jobs = self.scan_page_for_jobs()
        
        if jobs:
            print(f"   ✅ Found {len(jobs)} RELEVANT Targets.")
            page_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/projects/']")
            
            for i, job in enumerate(jobs):
                title = job.get('title', 'Unknown')
                budget = job.get('budget', 'N/A')
                print(f"\n   🎯 Target #{i+1}: {title} ({budget})")
                
                target_link = None
                for link in page_links:
                    try:
                        if title[:15].lower() in link.text.lower():
                            target_link = link
                            break
                    except: continue
                
                if target_link:
                    href = target_link.get_attribute('href')
                    if self.memory.is_processed(href):
                        print(f"      ⏭️  Skipping (Already Applied): {title}")
                        continue
                        
                    print(f"      🔗 Opening: {href}")
                    self.driver.execute_script(f"window.open('{href}', '_blank');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    time.sleep(5)
                    
                    self.apply_to_job(job, href)
                    
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    print("      zzz Sleeping 15s (Rate Limit Protection)...")
                    time.sleep(15)
                else:
                    print("      ⚠️ Could not find clickable link for this job.")
        else:
            print("   ⚠️ No targets identified on this page.")

    def close(self):
        self.driver.quit()
