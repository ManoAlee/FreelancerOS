
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: AUTOMOUS AGENT CORE (auto_main.py)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# "Zero-Touch" Infinite Loop
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import time
import sys
from hunter import Hunter
from brain import Brain
from hand import Hand

def main():
    print("🤖 STARTING AUTONOMOUS FREELANCER AGENT...")
    print("   Mode: Zero-Touch")
    print("   Press Ctrl+C to stop.")
    print("---------------------------------------------")
    
    hunter = Hunter()
    brain = Brain()
    hand = Hand()
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            print(f"\n⏳ [SYSTEM] Cycle #{cycle_count}")
            
            # 1. HUNT
            jobs = hunter.scan()
            
            # 2. ANALYZE & ACT
            for job in jobs:
                analysis = brain.analyze(job)
                
                if analysis:
                    # 3. WORK
                    work_result = brain.execute_work(analysis)
                    
                    # 4. DELIVER
                    hand.submit(analysis)
            
            # Wait for next cycle (short for demo, long for real)
            print("💤 [SYSTEM] Sleeping for 30s...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n🛑 [SYSTEM] Agent Stopped by User.")

if __name__ == "__main__":
    main()
