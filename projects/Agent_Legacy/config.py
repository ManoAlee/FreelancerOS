
import json
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# ⚙️ CONFIGURAÇÃO CENTRAL DO FREELANCER OS
CONFIG = {
    # 🆔 IDENTIDADE DO AGENTE
    "AGENT_NAME": "FreelancerOS Bot",
    "PERSONA_MODE": "SENIOR_DEV", 
    
    # 🔑 CREDENCIAIS
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    
    # 🧠 DEEPSEEK (Motor Principal - Novo)
    "DEEPSEEK_API_KEY": "sk-e9086873104e4a778ef567d02528753a",
    
    # 🤖 GOOGLE (Backup)
    "GOOGLE_API_KEY": "AIzaSyA0p3pqK4e-tjpdaE663Mw66J6feh20zt8",
    
    # 🏠 LOCAL AI (Ollama - Backup Offline)
    "USE_OLLAMA": True,
    "OLLAMA_MODEL": "llama3",
    "OLLAMA_URL": "http://localhost:11434/api/generate",
    
    # 🎯 ESTRATÉGIA DE PROSPECÇÃO
    "TARGET_PLATFORM": "Freelancer.com",
    "NICHE_KEYWORDS": ["python script", "web scraping", "automation", "excel vba", "landing page"],
    "MIN_BUDGET_USD": 30,
    "MAX_BUDGET_USD": 500,
    
    # 🛡️ SEGURANÇA
    "HUMAN_DELAY_MIN": 5, 
    "HUMAN_DELAY_MAX": 15,
    "WORK_HOURS_START": 9,
    "WORK_HOURS_END": 19,
    
    # 🕵️ CREDENCIAIS (Freelancer.com)
    "FREELANCER_USER": "Ale_meneses2004@hotmail.com",
    "FREELANCER_PASS": "@19L01e04#",
    
    # 📧 NOTIFICAÇÕES
    "NOTIFY_ON_MATCH": True,
    "OWNER_EMAIL": "ale_meneses2004@hotmail.com"
}

def load_config():
    return CONFIG
