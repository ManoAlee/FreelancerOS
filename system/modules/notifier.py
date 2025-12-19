# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Notification System
# Sends alerts for critical events
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

logger = logging.getLogger("Notifier")

class Notifier:
    """Handles notifications via email and other channels."""
    
    def __init__(self):
        self.email_enabled = os.getenv("NOTIFICATION_EMAIL_ENABLED", "false").lower() == "true"
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.from_email = os.getenv("MY_EMAIL", "")
        self.from_password = os.getenv("MY_PASSWORD", "")
        self.to_email = os.getenv("NOTIFICATION_EMAIL", self.from_email)
        
    def send_email(self, subject: str, body: str, priority: str = "normal"):
        """Send email notification."""
        if not self.email_enabled:
            logger.debug("Email notifications disabled")
            return False
        
        if not self.from_email or not self.from_password:
            logger.warning("Email credentials not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = f"[FreelancerOS] {subject}"
            
            # Add priority header
            if priority == "high":
                msg['X-Priority'] = '1'
                msg['Importance'] = 'high'
            
            # HTML body with styling
            html_body = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; }}
                        .header {{ background-color: #4CAF50; color: white; padding: 10px; }}
                        .content {{ padding: 20px; }}
                        .footer {{ background-color: #f1f1f1; padding: 10px; font-size: 12px; }}
                        .critical {{ color: #f44336; }}
                        .warning {{ color: #ff9800; }}
                        .info {{ color: #2196F3; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h2>🤖 FreelancerOS Agent</h2>
                    </div>
                    <div class="content">
                        <p>{body.replace(chr(10), '<br>')}</p>
                    </div>
                    <div class="footer">
                        <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p>This is an automated notification from FreelancerOS.</p>
                    </div>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.from_password)
                server.send_message(msg)
            
            logger.info(f"✅ Email notification sent: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False
    
    def notify_agent_started(self):
        """Notify that agent has started."""
        subject = "Agent Started"
        body = "The FreelancerOS agent has successfully started and is now operational."
        self.send_email(subject, body, "info")
    
    def notify_agent_stopped(self, reason: str = "Unknown"):
        """Notify that agent has stopped."""
        subject = "Agent Stopped"
        body = f"The FreelancerOS agent has stopped.\n\nReason: {reason}"
        self.send_email(subject, body, "high")
    
    def notify_error(self, error_message: str, context: Optional[str] = None):
        """Notify about an error."""
        subject = "Error Detected"
        body = f"An error was detected in the FreelancerOS agent.\n\n"
        body += f"Error: {error_message}\n"
        if context:
            body += f"\nContext: {context}"
        self.send_email(subject, body, "high")
    
    def notify_restart(self, attempt: int, max_attempts: int):
        """Notify about agent restart."""
        subject = f"Agent Restart (Attempt {attempt}/{max_attempts})"
        body = f"The FreelancerOS agent has been restarted.\n\n"
        body += f"Restart attempt: {attempt} of {max_attempts}\n"
        body += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.send_email(subject, body, "high")
    
    def notify_critical(self, message: str):
        """Notify about a critical event requiring intervention."""
        subject = "🚨 CRITICAL: Manual Intervention Required"
        body = f"A critical issue has occurred that requires manual intervention.\n\n"
        body += f"Issue: {message}\n"
        body += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        body += "Please check the agent logs and system status immediately."
        self.send_email(subject, body, "high")
    
    def notify_job_milestone(self, milestone: str, count: int):
        """Notify about job processing milestones."""
        subject = f"Milestone: {milestone}"
        body = f"The FreelancerOS agent has reached a milestone.\n\n"
        body += f"Milestone: {milestone}\n"
        body += f"Count: {count}\n"
        body += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.send_email(subject, body, "info")
    
    def notify_daily_summary(self, stats: dict):
        """Send daily summary of agent activity."""
        subject = "Daily Activity Summary"
        body = "FreelancerOS Agent - Daily Summary\n\n"
        
        total = sum(stats.values())
        body += f"Total Jobs Processed: {total}\n\n"
        
        for status, count in stats.items():
            percentage = (count / total * 100) if total > 0 else 0
            body += f"  {status}: {count} ({percentage:.1f}%)\n"
        
        body += f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.send_email(subject, body, "info")

# Global notifier instance
_notifier = None

def get_notifier() -> Notifier:
    """Get or create the global notifier instance."""
    global _notifier
    if _notifier is None:
        _notifier = Notifier()
    return _notifier
