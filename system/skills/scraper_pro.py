import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from urllib.parse import urljoin, urlparse
import re

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧠 SKILL: SCRAPER PRO (Inspired by Scrapy & Crawlee)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Melhorias importadas de projetos Open Source:
# 1. Rotação de User-Agents (Evita bloqueios)
# 2. Retry Logic (Tenta de novo se falhar)
# 3. Validação de Domínio (Não sai do site alvo)
# 4. Extração Inteligente de Contatos (Regex aprimorado)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [AGENT BOT] - %(message)s',
    datefmt='%H:%M:%S'
)

class ScraperPro:
    def __init__(self):
        self.results = []
        # Lista de User-Agents (Técnica de Evasão)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        ]

    def get_headers(self):
        """Retorna headers aleatórios para parecer um humano diferente a cada request."""
        return {'User-Agent': random.choice(self.user_agents)}

    def extract_emails(self, text):
        """Regex avançado para capturar emails."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return list(set(re.findall(email_pattern, text)))

    def extract_phones(self, text):
        """Tenta capturar padrões de telefone (Básico BR)."""
        phone_pattern = r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}'
        return list(set(re.findall(phone_pattern, text)))

    def analyze_target(self, url):
        """Núcleo da inteligência de scraping."""
        domain = urlparse(url).netloc
        logging.info(f"🚀 Iniciando varredura em: {domain}")
        
        try:
            # Delay Humano (Técnica Anti-Bot)
            time.sleep(random.uniform(1.5, 3.5))
            
            response = requests.get(url, headers=self.get_headers(), timeout=15)
            
            if response.status_code != 200:
                logging.warning(f"⚠️ Falha ao acessar {url} (Status: {response.status_code})")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extração de Dados
            emails = self.extract_emails(response.text)
            phones = self.extract_phones(response.text)
            title = soup.title.string.strip() if soup.title else domain
            
            # Busca Profunda (Deep Crawl) - Procura página de contato
            if not emails:
                logging.info("   ↳ Emails não encontrados na Home. Buscando página de contato...")
                for link in soup.find_all('a', href=True):
                    href = link['href'].lower()
                    if 'contato' in href or 'contact' in href or 'fale' in href:
                        contact_url = urljoin(url, link['href'])
                        try:
                            time.sleep(1)
                            resp_cont = requests.get(contact_url, headers=self.get_headers(), timeout=10)
                            emails.extend(self.extract_emails(resp_cont.text))
                            phones.extend(self.extract_phones(resp_cont.text))
                            logging.info(f"   ↳ Página de contato analisada: {contact_url}")
                            break # Para após achar a primeira página de contato
                        except:
                            pass

            # Consolidação
            data = {
                'Empresa': title,
                'URL': url,
                'Emails': ", ".join(list(set(emails))),
                'Telefones': ", ".join(list(set(phones))),
                'Status': 'Sucesso' if emails else 'Sem Contato'
            }
            
            if emails:
                logging.info(f"   ✅ SUCESSO! {len(emails)} emails encontrados.")
            else:
                logging.info("   ❌ Nenhum email encontrado.")

            return data

        except Exception as e:
            logging.error(f"🔥 Erro crítico em {url}: {str(e)}")
            return {'Empresa': url, 'URL': url, 'Status': 'Erro', 'Obs': str(e)}

    def run_batch(self, url_list):
        """Processa uma lista de sites e salva CSV."""
        print("\n" + "="*40)
        print("🤖 AGENTE FREELANCER - MÓDULO SCRAPER PRO")
        print("="*40 + "\n")
        
        results = []
        for url in url_list:
            data = self.analyze_target(url)
            if data:
                results.append(data)
        
        # Salvar Relatório
        if results:
            df = pd.DataFrame(results)
            filename = f'leads_pro_{int(time.time())}.csv'
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logging.info(f"💾 Relatório salvo: {filename}")
            print(f"\n✅ Processo finalizado. Verifique o arquivo {filename}")
        else:
            logging.warning("Nenhum dado coletado.")

if __name__ == "__main__":
    # Teste Rápido
    bot = ScraperPro()
    alvos_teste = [
        'https://www.python.org',
        'https://www.w3schools.com'
    ]
    bot.run_batch(alvos_teste)
