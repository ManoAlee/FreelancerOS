import time
import logging
import datetime
import random
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from system.config.config import CONFIG
from system.skills.scraper_pro import ScraperPro
from system.modules.email_sender import EmailSender

# Configuração de Log (Para você ver o que ele fez enquanto você dormia)
logging.basicConfig(
    filename='agent_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d/%m %H:%M:%S'
)

class AutonomousFreelancer:
    def __init__(self):
        self.scraper = ScraperPro()
        self.emailer = EmailSender(user=CONFIG['MY_EMAIL'], password=CONFIG['MY_PASSWORD'])
        self.leads_processed = 0
        print("🤖 AGENTE AUTÔNOMO INICIADO. Pressione Ctrl+C para parar.")
        logging.info("=== SESSÃO INICIADA ===")

    def is_work_time(self):
        """Verifica se está no horário de trabalho definido."""
        now = datetime.datetime.now().hour
        start, end = CONFIG['WORK_HOURS']
        return start <= now < end

    def sleep_mode(self):
        """Dorme para economizar recursos e evitar bloqueios."""
        sleep_time = random.randint(300, 900) # 5 a 15 minutos
        print(f"💤 Sem tarefas ou fora de horário. Dormindo por {int(sleep_time/60)} min...")
        time.sleep(sleep_time)

    def execute_cycle(self):
        """O Ciclo de Trabalho Infinito."""
        
        # 1. BUSCA (FIND)
        print(f"\n🔎 Buscando oportunidades para: {CONFIG['TARGET_NICHE']}...")
        # Simula busca baseada na config (Aqui conectaríamos o Google Search real)
        # Para o MVP, usamos uma lista fixa simulada baseada no nicho
        target_urls = [
            f"https://www.{CONFIG['TARGET_NICHE'].replace(' ', '')}.com.br",
            "https://www.exemplo-advocacia.com.br"
        ]
        
        for url in target_urls:
            if self.leads_processed >= CONFIG['MAX_LEADS_PER_DAY']:
                print("🛑 Meta diária atingida.")
                return

            # 2. ANÁLISE (READ)
            print(f"   👀 Analisando: {url}")
            data = self.scraper.analyze_target(url)
            
            if data and data['Status'] == 'Sucesso':
                email = data['Emails'].split(',')[0] if data['Emails'] else None
                
                if email:
                    # 3. EXECUÇÃO (ACT)
                    print(f"   🎯 Lead Encontrado: {data['Empresa']} ({email})")
                    logging.info(f"Lead Capturado: {data['Empresa']}")
                    
                    if CONFIG['AUTO_SEND_EMAIL']:
                        print(f"   🚀 Enviando proposta automática...")
                        # Personaliza o template
                        body = CONFIG['EMAIL_BODY'].replace("{empresa}", data['Empresa'])
                        self.emailer.send_campaign([{'email': email, 'name': data['Empresa']}], CONFIG['EMAIL_SUBJECT'], body)
                        logging.info(f"Proposta enviada para {email}")
                    else:
                        print(f"   💾 Salvo para revisão manual.")
                        logging.info(f"Lead salvo (sem envio): {email}")
                    
                    self.leads_processed += 1
                else:
                    print("   ❌ Sem contato disponível.")
            
            # Delay entre tarefas
            time.sleep(random.randint(10, 30))

    def start(self):
        while True:
            try:
                if self.is_work_time():
                    self.execute_cycle()
                    self.sleep_mode() # Pausa entre ciclos
                else:
                    print("🌙 Fora do horário de expediente.")
                    self.sleep_mode()
            except KeyboardInterrupt:
                print("\n🛑 Agente pausado pelo usuário.")
                break
            except Exception as e:
                logging.error(f"Erro Crítico: {e}")
                print(f"🔥 Erro: {e}. Reiniciando em 1 min...")
                time.sleep(60)

if __name__ == "__main__":
    bot = AutonomousFreelancer()
    bot.start()
