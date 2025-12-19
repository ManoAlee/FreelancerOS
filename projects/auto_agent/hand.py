
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-Agent: THE HAND (AI Writer System)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import time
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from system.ai_engine.core import LLMEngine
from system.ai_engine.prompts import HAND_WRITING_PROMPT

class Hand:
    def __init__(self):
        self.ai = LLMEngine(model="gpt-4o")

    def craft_proposal(self, analysis):
        """Generates a high-conversion proposal using LLM."""
        
        job_data = f"""
        Job Title: {analysis['job']['title']}
        Strategic Angle: {analysis['plan']}
        Skills to Highlight: {analysis['skills_used']}
        """
        
        proposal = self.ai.generate_text(
            system_prompt=HAND_WRITING_PROMPT,
            user_prompt=job_data
        )
        
        return proposal.strip()

    def submit(self, analysis):
        """Simulates submission."""
        
        print("\n✋ [HAND] AI Crafting Proposal...")
        proposal = self.craft_proposal(analysis)
        
        print("   ----------------------------------------")
        print(f"   {proposal.replace(chr(10), chr(10)+'   ')}")
        print("   ----------------------------------------")
        
        print("🚀 [HAND] Sending to Client...")
        time.sleep(1.5)
        print(f"✅ [HAND] SUCCESS: Proposal delivered to {analysis['job']['link']}")
        return True
