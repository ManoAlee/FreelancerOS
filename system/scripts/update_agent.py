import os

content = r'''import os
import time
import json
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

class GeminiClient:
    """
    Direct REST API Client for Google Gemini.
    Bypasses the deprecated/unstable Python SDK.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        # List of models to rotate through in case of Quota limits (429)
        self.models = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-flash-latest"]
        self.current_model_idx = 0
        self.headers = {"Content-Type": "application/json"}

    def _get_url(self):
        model = self.models[self.current_model_idx]
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

    def generate(self, prompt):
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        # Retry loop with model rotation
        max_retries = len(self.models) + 1
        for attempt in range(max_retries):
            url = self._get_url()
            try:
                response = requests.post(url, headers=self.headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    try:
                        return result['candidates'][0]['content']['parts'][0]['text']
                    except (KeyError, IndexError):
                        print(f"   ⚠️ Gemini Response Format Unexpected: {result}")
                        return None
                        
                elif response.status_code == 429:
                    current_model = self.models[self.current_model_idx]
                    print(f"   ⚠️ Quota Exceeded on {current_model}. Switching model...")
                    self.current_model_idx = (self.current_model_idx + 1) % len(self.models)
                    time.sleep(2)
                    continue
                    
                else:
                    print(f"   ⚠️ Gemini REST Error {response.status_code}: {response.text}")
                    return None
                    
            except Exception as e:
                print(f"   ⚠️ Gemini Connection Error: {e}")
                return None
                
        print("   ❌ All Gemini models exhausted.")
        return None

class FreelancerAgent:
    def __init__(self):
        """
        AI-Driven Browser Agent (The "Thinker")
        Uses Gemini (REST) or OpenAI to analyze page content.
        """
        self.openai_key = CONFIG.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.google_key = CONFIG.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        self.client = None
        self.gemini = None
        
        # Init Gemini (REST)
        if self.google_key:
            self.gemini = GeminiClient(self.google_key)
            print("   🧠 Cortex: Google Gemini (REST) Connected")

        # Init OpenAI
        if not self.gemini and self.openai_key:
            try:
                self.client = OpenAI(api_key=self.openai_key)
                print("   🧠 Cortex: OpenAI GPT-4o Connected")
            except:
                pass
        
        self.driver = self._setup_driver()

    def _setup_driver(self):
        options = Options()
        if CONFIG.get("HEADLESS", False):
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        # Suppress logging
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return webdriver.Chrome(options=options)

    def think(self, context, prompt):
        """
        The Agent's Inner Monologue.
        """
        full_prompt = f"CONTEXT:\n{context}\n\nTASK:\n{prompt}\n\nOUTPUT:\nJust the raw answer."
        
        # 1. Try Gemini
        if self.gemini:
            answer = self.gemini.generate(full_prompt)
            if answer:
                return answer.strip()
        
        # 2. Try OpenAI
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                return response.choices[0].message.content.strip()
            except:
                pass
        
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
            # Smart Selectors
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
            # Limit text to avoid payload limits
            clean_text = body_text.replace("\n", " ")[:8000]
            
            prompt = """
            Identify the current job listings in this text.
            For each job, extract: title, budget (if visible).
            Return ONLY a valid JSON list: [{"title": "Sample Job", "budget": "$30 - $250 USD"}].
            If no specific jobs are listed, return [].
            """
            
            print("   🧠 Analyzing with AI...")
            response = self.think(clean_text, prompt)
            
            if not response:
                return []
                
            # Clean JSON
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.replace("```", "")
                
            return json.loads(response)
        except Exception as e:
            print(f"   ⚠️ Analysis Error: {e}")
            return []

    def run_mission(self, mission_desc):
        print(f"\n🤖 MISSION START")
        
        # 1. Login
        user = CONFIG.get('FREELANCER_USER')
        pwd = CONFIG.get('FREELANCER_PASS')
        if user and "hotmail" in user:
            self.login(user, pwd)
        
        # 2. Search
        print(f"\n🔎 Searching for Targets...")
        # Use a simpler URL for stability
        self.driver.get("https://www.freelancer.com/jobs/python-automation/")
        time.sleep(5)
        
        # 3. AI Analysis
        jobs = self.scan_page_for_jobs()
        
        if jobs:
            print(f"   ✅ AI Found {len(jobs)} Active Targets.")
            for i, job in enumerate(jobs):
                title = job.get('title', 'Unknown')
                budget = job.get('budget', 'N/A')
                print(f"\n   🎯 Target #{i+1}: {title} ({budget})")
                
                # 4. Draft Bid
                bid_prompt = f"Write a professional, 2-sentence bid for: {title}"
                bid = self.think("I am an expert Python Automator.", bid_prompt)
                
                if bid:
                    print(f"      ✍️ Generated Bid: \"{bid}\"")
                else:
                    print(f"      ⚠️ Could not generate bid.")
        else:
            print("   ⚠️ No targets identified on this page.")
            print("      (Tip: Check if the search URL has results visible as text)")

    def close(self):
        self.driver.quit()
'''

with open('FreelancerOS/modules/agent_browser.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("File updated successfully.")
