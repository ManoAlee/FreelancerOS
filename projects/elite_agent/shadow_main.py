
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Elite Agent: SHADOW CORE (Silent Service)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import time
import logging
import sys
import os

# Setup Shadow Logging (File Only, No Console spam)
logging.basicConfig(
    filename='projects/elite_agent/shadow_ops.log',
    level=logging.INFO,
    format='%(asctime)s | %(module)s | %(message)s'
)

# Import Modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from projects.auto_agent.database import JobDatabase
from projects.auto_agent.hunter import Hunter
from prospector import Prospector
from negotiator import Negotiator

def run_service():
    # Silent Startup
    db = JobDatabase()
    hunter = Hunter()
    prospector = Prospector(config={})
    negotiator = Negotiator()
    
    logging.info("SHADOW SERVICE STARTED.")
    
    while True:
        try:
            # 1. Silent Hunt
            raw_jobs = hunter.scan() # Hunter prints, we might want to silence it or redirect stdout
            
            for job in raw_jobs:
                if not db.job_exists(job['id']):
                    db.add_job(job)
                    
                    # 2. Intel Analysis
                    intel = prospector.analyze_opportunity(job)
                    
                    if intel['decision'] == "ACCEPT":
                        # 3. Negotiation Strategy
                        persona = negotiator.select_persona(job['title'])
                        bid_content = negotiator.craft_bid(job, persona)
                        
                        # 4. Action (Log It / DB It)
                        score = int(intel['metrics']['roi'] * 10) # Mock conversion
                        db.mark_applied(job['id'], confidence=score)
                        
                        logging.info(f"APPLIED | {job['title']} | Persona: {persona.name} | ROI: {intel['metrics']['roi']:.2f}")
                    else:
                        db.mark_rejected(job['id'], reason=intel['reason'])
                        logging.info(f"REJECTED | {job['title']} | Reason: {intel['reason']}")
            
            time.sleep(45) # Deep sleep
            
        except Exception as e:
            logging.error(f"CRITICAL ERROR: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # Redirect stdout to devnull to truly be silent if needed, 
    # but for now we rely on the user just running it in background.
    print("...Shadow Service Running (Check logs)...")
    run_service()
