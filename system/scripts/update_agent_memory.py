import os
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
        # Check if URL is in applied list
        for job in self.history['applied_jobs']:
            if job['url'] == url:
                return True
        return False

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
        self.memory = Memory() # Initialize Memory
        
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
        
        # GLOBAL CONTEXT - The "Soul" of the Agent
        self.persona = """
        YOU ARE AN ELITE FREELANCER AGENT.
        YOUR NAME: FreelancerOS Bot.
        YOUR SKILLS: Python, Selenium, Web Scraping, Automation, Data Mining, Excel VBA, Bot Development.
        YOUR GOAL: Find high-value automation jobs and write winning proposals.
        TONE: Professional, confident, concise, result-oriented.
        NEVER hallucinate skills you don't have (like Video Editing or Translation).
        """

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
        # Inject Persona into every thought process to maintain context
        full_prompt = f"SYSTEM_PERSONA:\n{self.persona}\n\nCONTEXT:\n{context}\n\nTASK:\n{prompt}\n\nOUTPUT:\nJust the raw answer."
        
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
            clean_text = body_text.replace("\n", " ")[:12000]
            
            prompt = """
            Analyze the text and extract job listings.
            
            CRITERIA:
            1. FILTER: Keep ONLY jobs strictly related to: Python, Web Scraping, Automation, Bots, Scripting, Excel VBA.
            2. EXCLUDE: Video editing, Design, Translation, Writing, Marketing, Shopify Store Setup (unless coding involved).
            3. FORMAT: Return a valid JSON list: [{"title": "Job Title", "budget": "$XX"}].
            
            If no relevant jobs are found, return [].
            """
            
            print("   🧠 Analyzing & Filtering with AI...")
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

    def apply_to_job(self, job, job_url):
        """
        Navigates to the job page and places a bid.
        """
        print(f"      🤖 Analyzing Job Page: {self.driver.title}")
        
        # Generate Bid
        bid_prompt = f"Write a professional, concise (2-3 sentences) bid for: {job['title']}. Emphasize Python, Selenium, and Automation skills. No placeholders."
        bid = self.think("I am an expert Python Automator.", bid_prompt)
        
        if not bid:
            print("      ⚠️ Failed to generate bid text.")
            return

        print(f"      ✍️  Bid Prepared: \"{bid[:60]}...\"")
        
        try:
            # 1. Input Proposal
            print("      ⏳ Waiting for proposal form...")
            # Increased timeout to 15s and added more selectors
            desc_box = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#description, textarea[name='description'], textarea[placeholder*='proposal'], textarea.proposal-description"))
            )
            
            # Scroll into view to ensure visibility
            self.driver.execute_script("arguments[0].scrollIntoView(true);", desc_box)
            time.sleep(1)
            
            desc_box.clear()
            desc_box.send_keys(bid)
            time.sleep(1)
            
            # 2. Input Amount (Optional - often prefilled)
            # try:
            #     amount_box = self.driver.find_element(By.CSS_SELECTOR, "input.bid-amount, input[name='sum']")
            #     amount_box.clear()
            #     amount_box.send_keys("50") # Default or AI decided
            # except:
            #     pass
            
            # 3. Click Place Bid
            print("      👆 Looking for Place Bid button...")
            place_btn = self.driver.find_element(By.CSS_SELECTOR, "button#place-bid, button[data-id='place-bid-btn'], button.btn-primary, button.btn-success")
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", place_btn)
            time.sleep(1)
            
            # REAL SUBMISSION ENABLED
            place_btn.click()
            print("      🚀 BID SUBMITTED SUCCESSFULLY!")
            
            # SAVE TO MEMORY
            self.memory.add_applied(job_url, job['title'])
            
        except Exception as e:
            print(f"      ⚠️ Form interaction failed: {e}")

    def run_mission(self, mission_desc):
        print(f"\n🤖 MISSION START")
        
        # 1. Login
        user = CONFIG.get('FREELANCER_USER')
        pwd = CONFIG.get('FREELANCER_PASS')
        if user and "hotmail" in user:
            self.login(user, pwd)
        
        # 2. Search
        print(f"\n🔎 Searching for Targets...")
        self.driver.get("https://www.freelancer.com/jobs/python-automation/")
        time.sleep(5)
        
        # 3. AI Analysis
        jobs = self.scan_page_for_jobs()
        
        if jobs:
            print(f"   ✅ AI Found {len(jobs)} RELEVANT Targets.")
            
            # Find all project links on the search page to match against AI results
            # Freelancer links usually look like /projects/category/project-name
            page_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/projects/']")
            
            for i, job in enumerate(jobs):
                title = job.get('title', 'Unknown')
                budget = job.get('budget', 'N/A')
                print(f"\n   🎯 Target #{i+1}: {title} ({budget})")
                
                # 4. Match AI Job to Selenium Element
                target_link = None
                for link in page_links:
                    try:
                        # Fuzzy match: Check if first 15 chars of title exist in link text
                        if title[:15].lower() in link.text.lower():
                            target_link = link
                            break
                    except: continue
                
                if target_link:
                    href = target_link.get_attribute('href')
                    
                    # CHECK MEMORY
                    if self.memory.is_processed(href):
                        print(f"      ⏭️  Skipping (Already Applied): {title}")
                        continue
                        
                    print(f"      🔗 Opening: {href}")
                    
                    # Open in new tab
                    self.driver.execute_script(f"window.open('{href}', '_blank');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    time.sleep(5) # Wait for load
                    
                    # 5. Apply
                    self.apply_to_job(job, href)
                    
                    # Close tab and return
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    
                    # 6. Pause (Anti-Ban & Quota Management)
                    print("      zzz Sleeping 15s (Rate Limit Protection)...")
                    time.sleep(15)
                else:
                    print("      ⚠️ Could not find clickable link for this job.")
                    
        else:
            print("   ⚠️ No targets identified on this page.")
            print("      (Tip: Check if the search URL has results visible as text)")

    def close(self):
        self.driver.quit()
