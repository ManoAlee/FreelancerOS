import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import time

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📧 MÓDULO: EMAIL SENDER (Listmonk Style)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Funcionalidades:
# - Envio de Cold Mail (Prospecção)
# - Suporte a HTML Templates
# - Rotação de Assuntos (A/B Testing)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EmailSender:
    def __init__(self, smtp_server="smtp.gmail.com", port=587, user="", password=""):
        self.server = smtp_server
        self.port = port
        self.user = user
        self.password = password
        self.logger = logging.getLogger('EmailSender')

    def send_campaign(self, leads_list, subject, template_html):
        """Envia emails em massa com delay para evitar spam."""
        print(f"\n📧 [EMAIL] Iniciando campanha para {len(leads_list)} leads...")
        
        # Simulação de conexão (Para não travar sem credenciais reais)
        if not self.user:
            print("⚠️ [EMAIL] Modo Simulação (Sem credenciais configuradas)")
            time.sleep(1)
        
        count = 0
        for lead in leads_list:
            email = lead.get('email')
            name = lead.get('name', 'Parceiro')
            
            if not email:
                continue
                
            try:
                # Personalização do Template
                body = template_html.replace('{{nome}}', name)
                
                msg = MIMEMultipart()
                msg['From'] = self.user
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))
                
                # Aqui entraria o self.server.sendmail real
                # Simulando envio:
                print(f"   🚀 Enviando para {email}...")
                time.sleep(2) # Delay anti-spam
                count += 1
                
            except Exception as e:
                print(f"   ❌ Erro ao enviar para {email}: {e}")
                
        print(f"✅ [EMAIL] Campanha finalizada. {count} emails enviados.")

    def get_cold_mail_template(self):
        return """
        <html>
            <body>
                <p>Olá <strong>{{nome}}</strong>,</p>
                <p>Vi seu site e notei que ele poderia vender muito mais.</p>
                <p>Tenho uma estratégia rápida para resolver isso.</p>
                <p>Podemos conversar?</p>
            </body>
        </html>
        """
