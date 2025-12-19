#!/usr/bin/env python3
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Process Watchdog & Supervisor
# Monitors agent health and restarts if needed
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import sys
import os
import time
import subprocess
import signal
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
CHECK_INTERVAL = 60  # Check every 60 seconds
MAX_RESTART_ATTEMPTS = 5
RESTART_COOLDOWN = 300  # 5 minutes between restart attempts
LOG_FILE = "/app/logs/watchdog.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Watchdog")

class AgentWatchdog:
    """Monitors and supervises the FreelancerOS agent."""
    
    def __init__(self):
        self.process = None
        self.restart_count = 0
        self.last_restart = None
        self.running = True
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        logger.info("🐕 Watchdog initialized")
    
    def signal_handler(self, signum, frame):
        """Handle termination signals gracefully."""
        logger.info(f"📡 Received signal {signum}. Shutting down...")
        self.running = False
        if self.process:
            self.stop_agent()
    
    def start_agent(self):
        """Start the agent process."""
        try:
            logger.info("🚀 Starting FreelancerOS agent...")
            
            # Get project directory
            project_dir = Path(__file__).parent.parent.parent
            agent_script = project_dir / "projects" / "auto_agent" / "auto_main.py"
            
            if not agent_script.exists():
                logger.error(f"❌ Agent script not found: {agent_script}")
                return False
            
            # Start process
            self.process = subprocess.Popen(
                [sys.executable, str(agent_script)],
                cwd=str(project_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            )
            
            logger.info(f"✅ Agent started with PID: {self.process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start agent: {e}")
            return False
    
    def stop_agent(self):
        """Stop the agent process."""
        if not self.process:
            return
        
        try:
            logger.info(f"🛑 Stopping agent (PID: {self.process.pid})...")
            
            # Send SIGTERM first (graceful shutdown)
            self.process.terminate()
            
            # Wait up to 10 seconds
            try:
                self.process.wait(timeout=10)
                logger.info("✅ Agent stopped gracefully")
            except subprocess.TimeoutExpired:
                # Force kill if not responding
                logger.warning("⚠️  Agent not responding, forcing kill...")
                self.process.kill()
                self.process.wait()
                logger.info("✅ Agent force killed")
            
            self.process = None
            
        except Exception as e:
            logger.error(f"❌ Error stopping agent: {e}")
    
    def is_agent_healthy(self):
        """Check if agent is running and healthy."""
        if not self.process:
            return False
        
        # Check if process is still running
        if self.process.poll() is not None:
            logger.warning(f"⚠️  Agent process terminated with code: {self.process.returncode}")
            return False
        
        # Check database activity (last modified time)
        project_dir = Path(__file__).parent.parent.parent
        db_file = project_dir / "data" / "agent_memory.db"
        
        if db_file.exists():
            modified = datetime.fromtimestamp(db_file.stat().st_mtime)
            time_since = datetime.now() - modified
            
            # If database hasn't been modified in 10 minutes, might be stuck
            if time_since > timedelta(minutes=10):
                logger.warning(f"⚠️  Database not updated for {time_since.seconds // 60} minutes")
                # Don't restart immediately, just log the warning
                # The agent might be idle waiting for new jobs
        
        return True
    
    def should_restart(self):
        """Determine if we should attempt a restart."""
        # Check restart limit
        if self.restart_count >= MAX_RESTART_ATTEMPTS:
            logger.error(f"🚨 Max restart attempts ({MAX_RESTART_ATTEMPTS}) reached")
            return False
        
        # Check cooldown period
        if self.last_restart:
            time_since = datetime.now() - self.last_restart
            if time_since.seconds < RESTART_COOLDOWN:
                remaining = RESTART_COOLDOWN - time_since.seconds
                logger.warning(f"⏳ Restart cooldown: {remaining}s remaining")
                return False
        
        return True
    
    def restart_agent(self):
        """Restart the agent."""
        if not self.should_restart():
            return False
        
        logger.info("🔄 Attempting agent restart...")
        
        # Stop if running
        if self.process:
            self.stop_agent()
        
        # Wait a bit before restarting
        time.sleep(5)
        
        # Start agent
        if self.start_agent():
            self.restart_count += 1
            self.last_restart = datetime.now()
            logger.info(f"✅ Agent restarted (attempt {self.restart_count}/{MAX_RESTART_ATTEMPTS})")
            return True
        else:
            logger.error("❌ Failed to restart agent")
            return False
    
    def monitor(self):
        """Main monitoring loop."""
        logger.info("👁️  Starting monitoring loop...")
        
        # Initial start
        if not self.start_agent():
            logger.error("❌ Failed to start agent initially. Exiting.")
            return
        
        while self.running:
            try:
                time.sleep(CHECK_INTERVAL)
                
                logger.debug("🔍 Checking agent health...")
                
                if not self.is_agent_healthy():
                    logger.warning("⚠️  Agent is not healthy!")
                    
                    if not self.restart_agent():
                        logger.critical("🚨 Cannot recover agent. Manual intervention required.")
                        break
                else:
                    # Reset restart count on successful health check
                    if self.restart_count > 0:
                        logger.info(f"✅ Agent stable. Resetting restart counter (was {self.restart_count})")
                        self.restart_count = 0
                
            except Exception as e:
                logger.error(f"❌ Error in monitoring loop: {e}", exc_info=True)
                time.sleep(10)
        
        # Cleanup
        logger.info("👋 Watchdog shutting down...")
        if self.process:
            self.stop_agent()
        logger.info("✅ Watchdog stopped")

def main():
    """Entry point."""
    logger.info("="*60)
    logger.info("🐕 FreelancerOS Watchdog v1.0")
    logger.info("="*60)
    
    watchdog = AgentWatchdog()
    watchdog.monitor()

if __name__ == "__main__":
    main()
