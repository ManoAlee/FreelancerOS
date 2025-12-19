
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-Agent: THE HAND (Delivery System)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import time
import random

class Hand:
    def __init__(self):
        pass

    def craft_proposal(self, analysis):
        """Generates a proposal based on the Brain's analysis."""
        title = analysis['job']['title']
        skills = ", ".join(analysis['skills_used'])
        
        # Simple Template (Replace with LLM later)
        proposal = f"""
        Subject: Solution for {title}
        
        Hi,
        
        I detected your need for {skills}.
        My autonomous system has already generated a proof-of-concept.
        
        I can deliver this within 2 hours.
        
        Confidence Score: {analysis['confidence']}%
        """
        return proposal.strip()

    def submit(self, analysis):
        """Simulates submission."""
        proposal = self.craft_proposal(analysis)
        
        print("\n✋ [HAND] Crafting Proposal...")
        time.sleep(1)
        print("   ----------------------------------------")
        print(f"   {proposal.replace(chr(10), chr(10)+'   ')}")
        print("   ----------------------------------------")
        
        print("🚀 [HAND] Sending to Client...")
        time.sleep(1.5)
        print(f"✅ [HAND] SUCCESS: Proposal delivered to {analysis['job']['link']}")
        return True
