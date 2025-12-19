import sys
import os
import asyncio
import logging

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FreelancerOS.config import CONFIG
from FreelancerOS.modules.agent_browser import FreelancerAgent

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    print(f"""
    ╔════════════════════════════════════════╗
    ║  🤖 FREELANCER OS - AGENTE AUTÔNOMO    ║
    ║  Powered by Custom Selenium & GPT-4o   ║
    ╚════════════════════════════════════════╝
    """)

    agent = FreelancerAgent()
    
    # Constrói a missão com base na config
    keywords = ", ".join(CONFIG['NICHE_KEYWORDS'])
    
    mission = f"Find jobs for: {keywords}"
    
    # 1. Login Inicial
    user = CONFIG.get('FREELANCER_USER', '')
    if user and user != "seu_email_ou_usuario":
        pwd = CONFIG.get('FREELANCER_PASS', '')
        agent.login(user, pwd)
    else:
        print("   ⚠️ Modo Visitante (Sem Login). Configure config.py para logar.")
    
    try:
        agent.run_mission(mission)
    except KeyboardInterrupt:
        print("\n🛑 Agente desligado manualmente.")
    finally:
        input("\nPressione ENTER para fechar o navegador...")
        agent.close()

if __name__ == "__main__":
    main()
