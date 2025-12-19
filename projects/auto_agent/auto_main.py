
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AGENTE FREELANCER - AUTO MAIN (Self-Driving)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from system.ai_engine.autonomous_loop import AutonomousLoop
from system.config.config import CONFIG

def main():
    print("🤖 Booting FreelancerOS Self-Driving Agent [vΩ]...")
    
    # Define primary objective from config
    objective = f"Find and apply for jobs in niche: {CONFIG.get('TARGET_NICHE', 'General')}"
    
    # Initialize the vΩ Engine
    bot = AutonomousLoop(objective=objective)
    
    # Start the Infinite Cycle
    bot.run_forever()

if __name__ == "__main__":
    main()
