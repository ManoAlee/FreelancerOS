#!/usr/bin/env python3
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Health Monitor & Status Reporter
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from system.data_pipeline.recorder import JobRecorder

def print_header(text):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_database():
    """Check database connectivity and status."""
    try:
        recorder = JobRecorder()
        stats = recorder.get_stats()
        
        # Get database path from recorder
        db_path = os.path.join(os.path.dirname(recorder.conn.execute("PRAGMA database_list").fetchone()[2] or ""), "agent_memory.db")
        
        print("📊 Database Status: ✅ CONNECTED")
        print(f"   Location: {db_path}")
        return True, stats
    except Exception as e:
        print(f"📊 Database Status: ❌ ERROR")
        print(f"   Error: {e}")
        return False, {}

def check_logs():
    """Check log file status."""
    log_file = project_root / "logs" / "agent.log"
    
    if log_file.exists():
        size_mb = log_file.stat().st_size / (1024 * 1024)
        modified = datetime.fromtimestamp(log_file.stat().st_mtime)
        time_since = datetime.now() - modified
        
        print(f"📝 Log File: ✅ EXISTS")
        print(f"   Location: {log_file}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Last Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   ({time_since.seconds // 60} minutes ago)")
        
        # Check if log is recent (within last hour)
        if time_since < timedelta(hours=1):
            print("   Activity: 🟢 RECENT")
            return True
        else:
            print("   Activity: 🟡 STALE")
            return False
    else:
        print(f"📝 Log File: ❌ NOT FOUND")
        print(f"   Expected at: {log_file}")
        return False

def check_data_directory():
    """Check data directory status."""
    data_dir = project_root / "data"
    
    if data_dir.exists():
        files = list(data_dir.glob("*"))
        print(f"💾 Data Directory: ✅ EXISTS")
        print(f"   Location: {data_dir}")
        print(f"   Files: {len(files)}")
        return True
    else:
        print(f"💾 Data Directory: ❌ NOT FOUND")
        return False

def display_statistics(stats):
    """Display job statistics."""
    print_header("Job Statistics")
    
    if not stats:
        print("   No jobs recorded yet.")
        return
    
    total = sum(stats.values())
    print(f"   Total Jobs Tracked: {total}")
    print()
    
    for status, count in stats.items():
        percentage = (count / total * 100) if total > 0 else 0
        bar_length = int(percentage / 2)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        
        emoji = {
            "NEW": "🆕",
            "ANALYZED": "🧠",
            "APPLIED": "✅",
            "REJECTED": "❌",
            "ERROR": "⚠️"
        }.get(status, "📋")
        
        print(f"   {emoji} {status:12s}: {count:4d} [{bar}] {percentage:5.1f}%")

def check_docker():
    """Check if running in Docker."""
    if os.path.exists('/.dockerenv'):
        print("🐳 Environment: DOCKER")
        return True
    else:
        print("💻 Environment: NATIVE")
        return False

def main():
    """Main health check routine."""
    print_header("FreelancerOS Agent Health Monitor")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Environment check
    check_docker()
    print()
    
    # Component checks
    issues = []
    
    print_header("Component Status")
    
    db_ok, stats = check_database()
    if not db_ok:
        issues.append("Database connection failed")
    print()
    
    log_ok = check_logs()
    if not log_ok:
        issues.append("Log file issues detected")
    print()
    
    data_ok = check_data_directory()
    if not data_ok:
        issues.append("Data directory missing")
    print()
    
    # Statistics
    if db_ok:
        display_statistics(stats)
    
    # Overall status
    print_header("Overall Status")
    
    if not issues:
        print("   🎉 ALL SYSTEMS OPERATIONAL")
        print("   ✅ Agent is running smoothly")
        return 0
    else:
        print("   ⚠️  ISSUES DETECTED:")
        for issue in issues:
            print(f"      - {issue}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
