import os

content = r'''import os
import time
import json
import re
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI

# --- CONFIGURATION ---
try:
    import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from projects.Agent_Legacy.config import CONFIG
except ImportError:
    CONFIG = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"), 
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"), 
        "HEADLESS": False
    }

# --- PERSISTENT MEMORY ---
class Memory:
    def __init__(self, filename="mission_memory.json"):
        self.filename = filename
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return {"applied": [], "blacklisted": []}
        return {"applied": [], "blacklisted": []}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def remember_application(self, url, title):
        if url not in [x['url'] for x in self.data['applied']]:
            self.data['applied'].append({
                "url": url,
                "title": title,
                "timestamp": time.time()
            })
            self.save()

    def has_interacted(self, url):
        return any(x['url'] == url for x in self.data['applied'])

# --- AI CORE (GEMINI REST CLIENT) ---
class CortexAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = [
            "gemini-2.0-flash", 
            "gemini-2.0-flash-lite", 
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ]
        self.current_model_idx = 0
        self.headers = {"Content-Type": "application/json"}

    def _get_url(self):
        model = self.models[self.current_model_idx]
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

    def generate(self, prompt, context=""):
        full_prompt = f"CONTEXT:\n{context}\n\nINSTRUCTION:\n{prompt}"
        data = {"contents": [{"parts": [{"text": full_prompt}]}]}
        
        # Retry Logic with Model Rotation
        for attempt in range(len(self.models) + 1):
            url = self._get_url()
            try:
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
                
                if response.status_code == 200:
                    try:
                        return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                    except:
                        return None
                elif response.status_code == 429:
                    print(f"      ⚠️ Quota Limit ({self.models[self.current_model_idx]}). Rotating brain...")
                    self.current_model_idx = (self.current_model_idx + 1) % len(self.models)
                    time.sleep(2)
                else:
                    print(f"      ⚠️ AI Error {response.status_code}: {response.text[:100]}")
                    return None
            except Exception as e:
                print(f"      ⚠️ Connection Error: {e}")
                time.sleep(1)
        
        return None

# --- MAIN AGENT ---
class FreelancerAgent:
    def __init__(self):
        self.memory = Memory()
        self.ai = None
        
        # Init AI
        google_key = CONFIG.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if google_key:
            self.ai = CortexAI(google_key)
            print("   🧠 Cortex V2: Online (Google Gemini Cluster)")
        else:
            print("   ⚠️ Cortex V2: Offline (No API Key found)")

        self.driver = self._setup_driver()

    def _setup_driver(self):
        options = Options()
        if CONFIG.get("HEADLESS", False):
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return webdriver.Chrome(options=options)

    def login(self, username, password):
        print("\n🔑 Security: Authenticating...")
        self.driver.get("https://www.freelancer.com/login")
        time.sleep(3)

        if "login" not in self.driver.current_url:
            print("   ✅ Session Active.")
            return

        try:
            self.driver.find_element(By.CSS_SELECTOR, "input[name='user'], input[type='email']").send_keys(username)
            pwd = self.driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']")
            pwd.send_keys(password)
            pwd.send_keys(Keys.RETURN)
            time.sleep(5)
            print("   ✅ Login Sequence Complete.")
        except Exception as e:
            print(f"   ❌ Login Failed: {e}")

    def find_opportunities(self):
        """
        Hybrid Search:
        1. Scrapes raw links.
        2. Filters locally (Python) for keywords.
        3. Returns high-potential targets.
        """
        print("\n🔎 Radar: Scanning for High-Value Targets...")
        self.driver.get("https://www.freelancer.com/jobs/python-automation/")
        time.sleep(5)

        targets = []
        try:
            # Get all project cards
            cards = self.driver.find_elements(By.CSS_SELECTOR, "div.JobSearchCard-item")
            
            print(f"   👀 Visible Projects: {len(cards)}")
            
            keywords_good = ["python", "scraping", "automation", "bot", "script", "selenium", "excel", "api"]
            keywords_bad = ["design", "logo", "video", "translation", "writing", "article", "marketing"]

            for card in cards:
                try:
                    title_el = card.find_element(By.CSS_SELECTOR, "a.JobSearchCard-primary-heading-link")
                    title = title_el.text.strip()
                    url = title_el.get_attribute("href")
                    
                    # 1. Memory Check
                    if self.memory.has_interacted(url):
                        continue

                    # 2. Local Filter (Fast)
                    title_lower = title.lower()
                    if any(bad in title_lower for bad in keywords_bad):
                        continue
                    if not any(good in title_lower for good in keywords_good):
                        continue

                    targets.append({"title": title, "url": url})
                    
                except: continue

        except Exception as e:
            print(f"   ⚠️ Scan Error: {e}")

        print(f"   🎯 Filtered Targets: {len(targets)} potential jobs.")
        return targets[:5] # Process top 5 to avoid fatigue

    def execute_job(self, job):
        print(f"\n   🚀 Engaging Target: {job['title']}")
        
        # Open Job
        self.driver.execute_script(f"window.open('{job['url']}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(5)

        try:
            # Get Description
            desc_el = self.driver.find_element(By.CSS_SELECTOR, "div.PageProjectViewLogout-detail, div.Project-description")
            description = desc_el.text[:2000] # Limit context
            
            # 3. AI Evaluation (Deep)
            if self.ai:
                decision = self.ai.generate(
                    prompt="Is this job strictly for a Python Developer/Automator? Answer YES or NO only.",
                    context=f"Title: {job['title']}\nDescription: {description}"
                )
                
                if decision and "NO" in decision.upper():
                    print("      🚫 AI Analysis: Irrelevant. Skipping.")
                    self.memory.remember_application(job['url'], job['title']) # Mark as seen so we don't check again
                    return

                # 4. Generate Bid
                bid = self.ai.generate(
                    prompt="Write a winning proposal (2-3 sentences). Focus on: Python, Speed, Reliability. No placeholders.",
                    context=f"Job: {job['title']}\nDetails: {description}"
                )
            else:
                # Fallback if AI is dead
                bid = f"I am an expert in Python automation. I can build '{job['title']}' efficiently using my extensive library of scripts. Ready to start."

            if not bid:
                print("      ⚠️ Bid Generation Failed.")
                return

            print(f"      ✍️  Proposal: \"{bid[:50]}...\"")

            # 5. Submit
            self._place_bid(bid)
            self.memory.remember_application(job['url'], job['title'])

        except Exception as e:
            print(f"      ⚠️ Execution Error: {e}")
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def _place_bid(self, text):
        try:
            # Wait for form
            box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#description, textarea[name='description']"))
            )
            # Scroll & Type
            self.driver.execute_script("arguments[0].scrollIntoView(true);", box)
            time.sleep(1)
            box.clear()
            box.send_keys(text)
            
            # Click Button
            btn = self.driver.find_element(By.CSS_SELECTOR, "button#place-bid, button[data-id='place-bid-btn']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            btn.click()
            print("      ✅ BID SUBMITTED.")
        except:
            print("      ⚠️ Could not submit form (Button/Box not found).")

    def run(self):
        user = CONFIG.get('FREELANCER_USER')
        pwd = CONFIG.get('FREELANCER_PASS')
        if user: self.login(user, pwd)

        while True:
            targets = self.find_opportunities()
            
            if not targets:
                print("   zzz No targets found. Sleeping 60s...")
                time.sleep(60)
                continue

            for job in targets:
                self.execute_job(job)
                sleep_time = random.randint(10, 30)
                print(f"      zzz Cooling down ({sleep_time}s)...")
                time.sleep(sleep_time)

    def close(self):
        self.driver.quit()
'''

with open('FreelancerOS/modules/agent_browser.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("File updated successfully.")
