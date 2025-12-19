
import os
import json
import logging
from typing import Dict, Any, Optional

# Try to import openai, handle missing dependency
try:
    import openai
except ImportError:
    openai = None

from system.config.config import CONFIG
from system.ai_engine.prompts import MASTER_MCP_PROTOCOL

class LLMEngine:
    """
    The Central Intelligence Unit of FreelancerOS.
    Abstracts the AI provider (OpenAI, Gemini, Local) to provide a consistent interface.
    """
    
    def __init__(self, model: str = "gpt-4o"):
        self.logger = logging.getLogger("LLMEngine")
        self.api_key = CONFIG.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key and openai:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.logger.info(f"🧠 AI Engine Online. Model: {self.model}")
        else:
            self.logger.warning("⚠️ No API Key found or OpenAI not installed. Running in MOCK/HEURISTIC mode.")

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Generates a structured JSON response from the LLM.
        Enforces JSON schema via prompt engineering or API parameters.
        """
        # 🛡️ INJECT MASTER MCP PROTOCOL
        full_system_prompt = f"{MASTER_MCP_PROTOCOL}\n\n[SPECIFIC TASK INSTRUCTION]\n{system_prompt}"

        if not self.client:
            return self._mock_json_response(user_prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": full_system_prompt + "\n\nIMPORTANT: Return ONLY valid JSON."},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            self.logger.error(f"AI Generation Error: {e}")
            return self._mock_json_response(user_prompt, error=str(e))

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generates open-ended text (e.g., proposals, emails).
        """
        # 🛡️ INJECT MASTER MCP PROTOCOL
        full_system_prompt = f"{MASTER_MCP_PROTOCOL}\n\n[SPECIFIC TASK INSTRUCTION]\n{system_prompt}"

        if not self.client:
            return self._mock_text_response(user_prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"AI Generation Error: {e}")
            return f"Error creating proposal: {e}"

    def _mock_json_response(self, prompt: str, error: str = None) -> Dict[str, Any]:
        """Fallback logic for when AI is unavailable."""
        self.logger.info("🔮 Using Heuristic Fallback (Mock Brain)")
        
        # Simple heuristic simulation based on input length or keywords
        simulated_confidence = min(len(prompt) % 100, 95)
        
        return {
            "confidence_score": simulated_confidence,
            "decision": "GO" if simulated_confidence > 70 else "NO_GO",
            "reasoning": "Heuristic analysis: Keyword match detected (Simulated). " + (f"Error: {error}" if error else ""),
            "skills_matched": ["Python", "Automation", "Legacy_Skill"],
            "strategy": "Standard automated proposal."
        }

    def _mock_text_response(self, prompt: str) -> str:
        return """
        [MOCK PROPOSAL - AI OFFLINE]
        Subject: Application for your project
        
        Hello, I noticed your job posting and I believe my automation tools are a perfect fit.
        Please configure your API Key to unlock full personalized writing capabilities.
        """
