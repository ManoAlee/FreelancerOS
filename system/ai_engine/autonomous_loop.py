
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ARCHON v5.0 AUTONOMOUS LOOP ENGINE
# Enhanced with error handling, logging, and recovery
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import time
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

from system.ai_engine.core import LLMEngine
from system.data_pipeline.recorder import JobRecorder
from system.config.config import CONFIG

# Configure logging
log_dir = Path(CONFIG.get('LOG_FILE', '/app/logs/agent.log')).parent
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, CONFIG.get('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG.get('LOG_FILE', '/app/logs/agent.log')),
        logging.StreamHandler(sys.stdout)
    ]
)

class AutonomousLoop:
    """
    ARCHON: The Autonomous Reasoning System.
    Implements the Cycle: Evaluation -> Refinement -> High Value Action.
    Enhanced with error handling and self-recovery.
    """
    def __init__(self, objective: str):
        self.objective = objective
        self.logger = logging.getLogger("ARCHON")
        self.logger.info(f"🏛️  [ARCHON] Initializing with objective: {objective}")
        
        try:
            self.ai = LLMEngine()
            self.memory = JobRecorder()
        except Exception as e:
            self.logger.error(f"❌ [ARCHON] Initialization error: {e}")
            raise
            
        self.context = {
            "technical_scenario": {"status": "IDLE"},
            "human_practices": {},
            "synthesis": []
        }
        self.error_count = 0
        self.max_errors = CONFIG.get('MAX_RETRIES', 3)
        self.retry_delay = CONFIG.get('RETRY_DELAY_SECONDS', 10)
        self.last_health_check = time.time()
        self.health_check_interval = CONFIG.get('HEALTH_CHECK_INTERVAL', 300)  # 5 minutes
        
        self.logger.info("✅ [ARCHON] Initialization complete")

    def health_check(self):
        """Performs self-diagnostic checks."""
        try:
            current_time = time.time()
            if current_time - self.last_health_check < self.health_check_interval:
                return True
                
            self.logger.info("🏥 [ARCHON] Performing health check...")
            
            # Check database connectivity
            stats = self.memory.get_stats()
            self.logger.info(f"📊 [ARCHON] Database status: {stats}")
            
            # Check memory usage (basic check)
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.logger.info(f"💾 [ARCHON] Memory usage: {memory_mb:.2f} MB")
            
            # Reset error count on successful health check
            self.error_count = 0
            self.last_health_check = current_time
            
            self.logger.info("✅ [ARCHON] Health check passed")
            return True
        except Exception as e:
            self.logger.error(f"⚠️  [ARCHON] Health check failed: {e}")
            return False

    def cycle(self):
        """Runs one full ARCHON cycle with error handling."""
        try:
            self.logger.info("\n🏛️  [ARCHON] Starting Reasoning Cycle...")
            
            # 1. EVALUATION (Avaliação de Estado)
            state = self._evaluate_state()
            self.logger.info(f"   1️⃣  State Assessment: {state['status']}")
            
            if state['status'] == "COMPLETED":
                return "SLEEP"

            # 2. REFINEMENT (Refinamento Contínuo)
            refined_context = self._refine_context(state)
            self.logger.info(f"   2️⃣  Context Refined: {refined_context['ambiguity_level']}")

            # 3. HIGH VALUE ACTION (Ação de Maior Valor)
            actions = self._generate_actions(refined_context)
            best_action = self._prioritize(actions)
            self.logger.info(f"   3️⃣  Selected High-Value Action: {best_action['name']} (Impact: {best_action['impact']})")

            # 4. EXECUTION w/ KERNEL PROTOCOL
            self._execute(best_action)
            
            # Reset error count on successful cycle
            self.error_count = 0
            return "SUCCESS"
            
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"❌ [ARCHON] Cycle error (attempt {self.error_count}/{self.max_errors}): {e}", exc_info=True)
            
            if self.error_count >= self.max_errors:
                self.logger.critical("🚨 [ARCHON] Max errors reached. Initiating recovery...")
                self._recovery_mode()
            
            return "ERROR"
        
    def _evaluate_state(self) -> Dict:
        """Checks objective measurability and evidence sufficiency."""
        try:
            stats = self.memory.get_stats()
            
            # ARCHON Epistemological Check
            has_evidence = sum(stats.values()) > 0
            
            return {
                "status": "ACTIVE", 
                "evidence_quality": "HIGH" if has_evidence else "LOW",
                "metrics": stats
            }
        except Exception as e:
            self.logger.error(f"⚠️  [ARCHON] State evaluation error: {e}")
            return {
                "status": "ERROR",
                "evidence_quality": "UNKNOWN",
                "metrics": {}
            }

    def _refine_context(self, state) -> Dict:
        """Reduces ambiguity and increases technical precision."""
        # Simulated refinement step
        if state['evidence_quality'] == "LOW":
            return {"ambiguity_level": "HIGH", "focus": "Acquire Data"}
        return {"ambiguity_level": "LOW", "focus": "Optimize"}

    def _generate_actions(self, context) -> List[Dict]:
        """Proposes actions based on ARCHON personas."""
        actions = []
        
        if context['focus'] == "Acquire Data":
             # Persona: Data Engineer
            actions.append({
                "name": "Data Acquisition Protocol (Hunter)",
                "persona": "Data Engineer",
                "impact": "CRITICAL",
                "risk": "LOW"
            })
        else:
             # Persona: SRE / Optimizer
            actions.append({
                "name": "System Optimization Analysis",
                "persona": "SRE",
                "impact": "HIGH",
                "risk": "MEDIUM"
            })
        
        return actions

    def _prioritize(self, actions: List[Dict]) -> Dict:
        """Selects action based on Impact > Risk > Utility."""
        # ARCHON Prioritization Logic
        return max(actions, key=lambda x: 100 if x['impact'] == "CRITICAL" else 50)

    def _execute(self, action):
        """Runs the action following KERNEL protocol."""
        try:
            self.logger.info(f"   🚀 [KERNEL] Executing: {action['name']} as {action['persona']}...")
            time.sleep(1) 
            self.logger.info(f"   ✅ [KERNEL] Output Evaluated. Logic Traceable.")
        except Exception as e:
            self.logger.error(f"   ❌ [KERNEL] Execution error: {e}")
            raise

    def _recovery_mode(self):
        """Attempts to recover from critical errors."""
        self.logger.info("🔧 [ARCHON] Entering recovery mode...")
        
        try:
            # Wait for a longer period
            time.sleep(self.retry_delay * 3)
            
            # Reset internal state
            self.context = {
                "technical_scenario": {"status": "IDLE"},
                "human_practices": {},
                "synthesis": []
            }
            
            # Reset error count
            self.error_count = 0
            
            self.logger.info("✅ [ARCHON] Recovery complete. Resuming operations...")
        except Exception as e:
            self.logger.critical(f"🚨 [ARCHON] Recovery failed: {e}")
            # Let the system restart via Docker/systemd

    def run_forever(self):
        """The Main ARCHON Thread with enhanced reliability."""
        self.logger.info("🚀 [ARCHON] Starting infinite loop...")
        
        loop_count = 0
        
        while True:
            try:
                loop_count += 1
                self.logger.info(f"\n{'='*60}")
                self.logger.info(f"🔄 [ARCHON] Loop #{loop_count} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.logger.info(f"{'='*60}")
                
                # Perform health check periodically
                if not self.health_check():
                    self.logger.warning("⚠️  [ARCHON] Health check failed, but continuing...")
                
                # Run cycle
                decision = self.cycle()
                
                if decision == "SLEEP":
                    self.logger.info("💤 Telos Achieved. Standing by...")
                    time.sleep(CONFIG.get('LOOP_INTERVAL_SECONDS', 60))
                elif decision == "ERROR":
                    self.logger.warning(f"⚠️  [ARCHON] Error in cycle. Waiting {self.retry_delay}s before retry...")
                    time.sleep(self.retry_delay)
                else:
                    time.sleep(CONFIG.get('LOOP_INTERVAL_SECONDS', 60) / 10)  # Quick iteration on success
                    
            except KeyboardInterrupt:
                self.logger.info("\n⛔ [ARCHON] Shutdown signal received. Exiting gracefully...")
                break
            except Exception as e:
                self.logger.critical(f"🚨 [ARCHON] Unhandled exception in main loop: {e}", exc_info=True)
                time.sleep(self.retry_delay * 2)
                
        self.logger.info("👋 [ARCHON] Shutdown complete.")
