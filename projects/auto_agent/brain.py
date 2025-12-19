
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-Agent: THE BRAIN (Symbiotic AI Core)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import sys
import os
import json

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from system.ai_engine.cognitive_pipeline import CognitivePipeline
from system.mcp_core.server import MCPServer
from freelanceros.modules import business_math, text_data, system_files, media_web

class Brain:
    def __init__(self):
        # 🧠 Upgrade: Using 7-Layer Cognitive Architecture
        self.cognition = CognitivePipeline()
        
        # 🔌 INITIALIZE INTERNAL MCP SERVER
        self.mcp = MCPServer()
        self._load_tools()

    def _load_tools(self):
        """Auto-discovers capabilities from the OS."""
        print("🔌 [BRAIN] Booting MCP Server & Discovering Tools...")
        self.mcp.auto_discover(business_math)
        self.mcp.auto_discover(text_data)
        self.mcp.auto_discover(system_files)
        self.mcp.auto_discover(media_web)
        print(f"🔌 [BRAIN] Registered {len(self.mcp.list_tools())} tools.")

    def analyze(self, job):
        """
        Passes the job through the Semantic Cognitive Pipeline.
        """
        print(f"🧠 [BRAIN] Symbiotic Cycle Start: '{job['title']}'")
        
        # Prepare Input Packet
        raw_input = {
            "type": "JOB_OPPORTUNITY",
            "text": f"Title: {job['title']}\nDescription: {job.get('summary', '')}",
            "metadata": job,
            "available_tools": [t['name'] for t in self.mcp.list_tools()]
        }
        
        # ⚡ EXECUTE COGNITIVE PIPELINE
        result = self.cognition.process_input(raw_input)
        
        if "error" in result:
             print(f"❌ [BRAIN] Blocked by Risk Layer: {result['error']}")
             return None

        # Transform generic result into Agent Action Plan
        # (Assuming the pipeline returns a 'final_content' or similar structure)
        # For MVP, we bridge the gap manually or assume pipeline returns a dict
        
        # Mocking the pipeline return for now as we build it out fully
        confidence = result.get("quality_score", 0)
        
        print(f"✅ [BRAIN] Symbiotic Verdict: GO (Confidence: {confidence}%)")
        
        return {
            "job": job,
            "confidence": confidence,
            "plan": "Executed Symbiotic Strategy",
            "skills_used": ["Cognitive Analysis"],
            "ai_analysis": result
        }

    def execute_work(self, task):
        return "Work simulated successfully."
