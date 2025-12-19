# 🤖 Zero-Touch Freelancer Agent: "The Autonomist"

**Status**: OPERATIONAL | **Architecture**: Hunter-Brain-Hand

## Overview

This is not a tool you use. It is a system that works for you.
It runs in an infinite loop, monitoring the web for jobs, analyzing them against its internal skill library (`FreelancerOS`), and autonomously crafting proposals.

## 🏗️ Architecture

1.  **👁️ The Hunter (`hunter.py`)**
    - Monitors RSS feeds (WeWorkRemotely, Upwork\*) 24/7.
    - Filters duplicates automatically.
2.  **🧠 The Brain (`brain.py`)**
    - Reads Job Descriptions.
    - Matches keywords to the 220+ tools in `FreelancerOS`.
    - Decides: "Can I do this?"
3.  **✋ The Hand (`hand.py`)**
    - Generates hyper-persuasive proposals based on the matching skills.
    - Simulates submission/email delivery.

## 🚀 How to Run (Zero-Touch Mode)

1.  Open your terminal.
2.  Run the infinite loop:
    ```bash
    python projects/auto_agent/auto_main.py
    ```
3.  Minimize the window and go to sleep.

## 🎛️ Configuration

- **Add Feeds**: Edit `projects/auto_agent/hunter.py` and add URLs to the `SOURCES` list.
- **Tweak Logic**: Edit `projects/auto_agent/brain.py` to add new keyword mappings.

_Note: This agent uses the "FreelancerOS" core as its skill engine._
