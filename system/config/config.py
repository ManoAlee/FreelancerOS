# ⚙️ CENTRAL DE COMANDO (Configure uma vez, esqueça depois)
import os
from typing import List

def get_env_bool(key: str, default: bool = False) -> bool:
    """Convert environment variable to boolean."""
    value = os.getenv(key, str(default))
    return value.lower() in ('true', '1', 'yes', 'on')

def get_env_int(key: str, default: int) -> int:
    """Convert environment variable to integer."""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default

def get_env_list(key: str, default: List[str] = None) -> List[str]:
    """Convert comma-separated environment variable to list."""
    value = os.getenv(key, '')
    if value:
        return [item.strip() for item in value.split(',')]
    return default or []

# RSS Feeds from environment or defaults
rss_feeds = []
for i in range(1, 11):  # Support up to 10 RSS feeds
    feed = os.getenv(f'RSS_FEED_{i}', '')
    if feed:
        rss_feeds.append(feed)

if not rss_feeds:
    rss_feeds = [
        "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-design-jobs.rss"
    ]

CONFIG = {
    # 🎯 QUEM VAMOS ATACAR?
    "TARGET_NICHE": os.getenv("TARGET_NICHE", "advogados em são paulo"),
    "MAX_LEADS_PER_DAY": get_env_int("MAX_LEADS_PER_DAY", 50),
    
    # 🤖 COMPORTAMENTO DO ROBÔ
    "MODE": os.getenv("MODE", "AGGRESSIVE"),  # 'SAFE' (Lento/Seguro) ou 'AGGRESSIVE' (Rápido)
    "WORK_HOURS": [
        get_env_int("WORK_HOURS_START", 9),
        get_env_int("WORK_HOURS_END", 18)
    ],
    "LOOP_INTERVAL_SECONDS": get_env_int("LOOP_INTERVAL_SECONDS", 60),
    "MAX_RETRIES": get_env_int("MAX_RETRIES", 3),
    "RETRY_DELAY_SECONDS": get_env_int("RETRY_DELAY_SECONDS", 10),
    
    # 📧 AUTOMAÇÃO DE VENDAS
    "AUTO_SEND_EMAIL": get_env_bool("AUTO_SEND_EMAIL", True),
    "MY_EMAIL": os.getenv("MY_EMAIL", "seu_email@gmail.com"),
    "MY_PASSWORD": os.getenv("MY_PASSWORD", "sua_senha_de_app"),
    "SMTP_HOST": os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "SMTP_PORT": get_env_int("SMTP_PORT", 587),
    
    # 🕷️ FONTES DE DADOS
    "SOURCES": rss_feeds,
    
    # 🛡️ SECURITY & FILTERS
    "MIN_CONFIDENCE_SCORE": get_env_int("MIN_CONFIDENCE_SCORE", 75),
    "BLACKLIST_WORDS": get_env_list("BLACKLIST_WORDS", ["senior", "lead", "architect"]),
    "HEADLESS_BROWSER": get_env_bool("HEADLESS_BROWSER", True),
    
    # 📊 LOGGING
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "LOG_FILE": os.getenv("LOG_FILE", "/app/logs/agent.log"),
    
    # 📝 MODELO DE PROPOSTA (O Robô preenche sozinho)
    "EMAIL_SUBJECT": "Parceria para {empresa}",
    "EMAIL_BODY": """
    Olá, vi que a {empresa} tem um grande potencial.
    Sou um agente autônomo especializado em web.
    Criei um pré-projeto para vocês. Podemos conversar?
    """
}
