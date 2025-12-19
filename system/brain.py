import os
import sys
import time
import shutil
import logging

# Adiciona diretórios ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importação dos Módulos (O "Merge" dos Projetos GitHub)
from skills.scraper_pro import ScraperPro
from modules.social_bot import SocialBot
from modules.browser_bot import BrowserBot
from modules.email_sender import EmailSender
from modules.marketing_automator import WorkflowAutomator

# Configuração Global
logging.basicConfig(level=logging.INFO, format='%(message)s')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("""
    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
    ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
    ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
    ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
    
    🤖 SUPER AGENTE FREELANCER v3.0 (ALL-IN-ONE)
    --------------------------------------------------
    Integração Total: Scraping + Social + Browser + Web
    """)

def run_scraper():
    print("\n🕷️ [1] LEAD HUNTER (Extrator de Dados)")
    urls = input("   URLs alvo (separadas por vírgula): ").split(',')
    if urls[0]:
        bot = ScraperPro()
        bot.run_batch([u.strip() for u in urls])
    input("\n[Enter] para voltar...")

def run_social():
    print("\n❤️ [2] SOCIAL BOT (Engajamento Automático)")
    tag = input("   Qual Hashtag atacar? (ex: marketing): ")
    if tag:
        bot = SocialBot()
        bot.login("Instagram", "seu_usuario", "******")
        bot.engage_hashtag(tag, count=5)
    input("\n[Enter] para voltar...")

def run_browser():
    print("\n🖥️ [3] BROWSER BOT (Automação Web)")
    print("   Exemplo: Preencher formulário de contato em massa.")
    url = input("   URL do Formulário: ")
    if url:
        bot = BrowserBot()
        bot.open_browser()
        data = {'Nome': 'Agente Frela', 'Email': 'contato@agente.com', 'Msg': 'Olá!'}
        bot.fill_form(url, data)
    input("\n[Enter] para voltar...")

def run_landing_page():
    print("\n🚀 [4] GERADOR DE SITES (Venda Rápida)")
    name = input("   Nome do Cliente: ")
    if name:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src = os.path.join(base, 'projects', 'landing_page_job')
        dst = os.path.join(base, 'projects', f'site_{name.replace(" ", "_").lower()}')
        try:
            shutil.copytree(src, dst)
            print(f"   ✅ Site criado em: {dst}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    input("\n[Enter] para voltar...")

def run_email_marketing():
    print("\n📧 [5] EMAIL MARKETING (Disparo em Massa)")
    print("   Simulando envio para lista de leads...")
    leads = [{'email': 'cliente1@teste.com', 'name': 'João'}, {'email': 'cliente2@teste.com', 'name': 'Maria'}]
    
    sender = EmailSender(user="seu_email@gmail.com") # Configurar depois
    template = sender.get_cold_mail_template()
    sender.send_campaign(leads, "Oportunidade de Negócio", template)
    input("\n[Enter] para voltar...")

def run_workflow():
    print("\n⚡ [6] AUTOMAÇÃO DE MARKETING (Workflow)")
    print("   Simulando funil de vendas...")
    lead = {'email': 'novo_lead@empresa.com', 'empresa': 'Tech Solutions'}
    
    automator = WorkflowAutomator()
    automator.run_sales_funnel(lead)
    input("\n[Enter] para voltar...")

def main():
    while True:
        clear_screen()
        print_header()
        print("1. 🕷️  Lead Hunter (Scraper)")
        print("2. ❤️  Social Bot (Instagram/X)")
        print("3. 🖥️  Browser Bot (Formulários)")
        print("4. 🚀  Gerador de Sites (Landing Page)")
        print("5. 📧  Email Marketing (Cold Mail)")
        print("6. ⚡  Automação de Workflow (Funil)")
        print("0. ❌  Sair")
        
        opt = input("\nCOMANDO > ")
        
        if opt == '1': run_scraper()
        elif opt == '2': run_social()
        elif opt == '3': run_browser()
        elif opt == '4': run_landing_page()
        elif opt == '5': run_email_marketing()
        elif opt == '6': run_workflow()
        elif opt == '0': break

if __name__ == "__main__":
    main()
