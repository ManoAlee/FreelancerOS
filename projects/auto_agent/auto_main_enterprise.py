
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: ENTERPRISE AGENT CORE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import time
import yaml
from hunter import Hunter
from brain_enterprise import EnterpriseBrain
from database import JobDatabase
from hand import Hand # Use existing Hand for now

def main():
    print("🏢 INITIALIZING ENTERPRISE AGENT v2.0...")
    
    # 1. Load Config
    try:
        with open("projects/auto_agent/config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        print("✅ Config Loaded.")
    except Exception as e:
        print(f"❌ Config Error: {e}")
        return

    # 2. Init Subsystems
    db = JobDatabase()
    hunter = Hunter() # Hunter needs to read config feeds ideally, but we kept it simple for now
    brain = EnterpriseBrain()
    hand = Hand()
    
    print("✅ Database Connected.")
    print("✅ Brain Calibrated.")
    print("---------------------------------------------")
    print(f"   Targeting Feeds: {len(config['feeds'])}")
    print(f"   Min Score: {config['filters']['min_confidence_score']}")
    print("---------------------------------------------")

    while True:
        try:
            print("\n🔄 [CYCLE] Syncing...")
            
            # 1. HUNT (Modified to use Config Feeds)
            # Monkey-patching source list for this run
            import hunter as h_mod
            h_mod.SOURCES = config['feeds']
            
            raw_jobs = hunter.scan()
            
            new_count = 0
            for job in raw_jobs:
                # 2. PERSIST (Add to DB)
                if db.add_job(job):
                    new_count += 1
                    
                    # 3. ANALYZE (Brain)
                    analysis = brain.evaluate(job)
                    
                    if analysis['decision'] == "APPLY":
                        print(f"   ⭐ HIGHLIGHT: {job['title']} (Score: {analysis['score']})")
                        
                        # 4. EXECUTE (Hand)
                        hand.submit({
                            "job": job,
                            "confidence": analysis['score'],
                            "skills_used": [analysis['reason']] 
                        })
                        
                        db.mark_applied(job['id'], analysis['score'])
                        
                    else:
                        print(f"   Start pass: {job['title']} (Score: {analysis['score']})")
                        db.mark_rejected(job['id'])
            
            if new_count == 0:
                print("   (No new unique jobs found)")
                
            stats = db.get_stats()
            print(f"📊 DB Stats: {stats}")
            
            interval = config['agent']['loop_interval_seconds']
            print(f"💤 Sleeping {interval}s...")
            time.sleep(interval)

        except KeyboardInterrupt:
            print("🛑 Agent Shutting Down.")
            break
        except Exception as e:
            print(f"⚠️ Critical Loop Error: {e}")
            time.sleep(10) # Prevent rapid crash loop

if __name__ == "__main__":
    main()
