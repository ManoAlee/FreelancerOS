import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🕷️ LEAD HUNTER PRO - EMAIL & CONTACT EXTRACTOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Descrição: Varre uma lista de sites em busca de emails e contatos.
# Ideal para: Criar listas de prospecção (Cold Mailing).
# Preço de Venda do Serviço: $50 - $150 por 1000 leads.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import re
from urllib.parse import urljoin

class LeadScraper:
    def __init__(self, url_list):
        self.url_list = url_list
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.results = []
        print("🛡️ MODO RESPONSÁVEL ATIVADO: Respeitando delays e servidores.")

    def check_robots_txt(self, url):
        """Verificação básica de ética (Opcional, mas recomendada)."""
        # Em um projeto real, usaríamos a lib urllib.robotparser
        # Aqui apenas simulamos a consciência da existência disso.
        pass

    def extract_emails(self, text):
        """Usa Regex para encontrar emails no texto HTML."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return list(set(re.findall(email_pattern, text)))

    def process_site(self, url):
        """Acessa o site e busca contatos."""
        
        # Delay ético para não sobrecarregar o servidor alvo
        time.sleep(random.uniform(2, 4)) 
        
        print(f"🔍 Analisando: {url}...")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 1. Tenta pegar o título (Nome da Empresa)
                title = soup.title.string.strip() if soup.title else url
                
                # 2. Busca emails na home
                emails = self.extract_emails(response.text)
                
                # 3. Tenta encontrar página de contato
                contact_link = None
                for link in soup.find_all('a', href=True):
                    if 'contato' in link.text.lower() or 'contact' in link.text.lower():
                        contact_link = urljoin(url, link['href'])
                        break
                
                # Se achou link de contato, varre ele também
                if contact_link:
                    try:
                        print(f"   ➡️ Visitando página de contato: {contact_link}")
                        contact_resp = requests.get(contact_link, headers=self.headers, timeout=10)
                        more_emails = self.extract_emails(contact_resp.text)
                        emails.extend(more_emails)
                    except:
                        pass

                # Limpa e salva
                unique_emails = list(set(emails))
                
                if unique_emails:
                    print(f"   ✅ SUCESSO! {len(unique_emails)} emails encontrados.")
                    self.results.append({
                        'Empresa': title,
                        'Website': url,
                        'Emails': ", ".join(unique_emails),
                        'Status': 'Encontrado'
                    })
                else:
                    print("   ⚠️ Nenhum email visível.")
                    self.results.append({
                        'Empresa': title,
                        'Website': url,
                        'Emails': '',
                        'Status': 'Sem Email'
                    })
            else:
                print(f"   ❌ Erro: Status {response.status_code}")

        except Exception as e:
            print(f"   ❌ Erro de conexão: {str(e)[:50]}")

    def save_to_csv(self, filename='leads_encontrados.csv'):
        if not self.results:
            print("Nenhum dado para salvar.")
            return
        
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 Relatório salvo em: {filename}")
        print(df.head())

# ==========================================
# 🚀 ÁREA DE EXECUÇÃO
# ==========================================
if __name__ == "__main__":
    # LISTA DE ALVOS (Exemplo: Empresas locais que precisam de site)
    # Dica: Pegue esses links do Google Maps ou de um diretório local
    alvos = [
        'https://www.advocaciaexemplo.com.br', # Exemplo (vai falhar, mas ilustra)
        'https://www.python.org',              # Teste Real
        'https://www.freelancer.com',          # Teste Real
        # Adicione aqui os sites dos seus potenciais clientes
    ]
    
    print(f"🚀 Iniciando Lead Hunter Pro em {len(alvos)} sites...\n")
    bot = LeadScraper(alvos)
    for site in alvos:
        bot.process_site(site)
        time.sleep(1) # Respeitar o servidor
        
    bot.save_to_csv()

    def run(self, pages=1):
        """Executa o fluxo principal."""
        print(f"🚀 Iniciando Scraping em: {self.base_url}")
        
        for page in range(1, pages + 1):
            print(f"--- Processando Página {page} ---")
            url = f"{self.base_url}/catalogue/page-{page}.html" if page > 1 else f"{self.base_url}/catalogue/page-1.html"
            html = self.fetch_page(url)
            if html:
                self.parse_books(html)
        
        self.save_data()

    def save_data(self):
        """Salva em CSV e Excel (Formatos que clientes amam)."""
        if not self.data:
            print("⚠️ Nenhum dado para salvar.")
            return

        df = pd.DataFrame(self.data)
        
        # Salvar CSV
        csv_path = 'projects/scraper_job/output_data.csv'
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        # Salvar Excel (Client favorite)
        excel_path = 'projects/scraper_job/output_data.xlsx'
        try:
            df.to_excel(excel_path, index=False)
            print(f"📂 Excel salvo: {excel_path}")
        except Exception as e:
            print(f"⚠️ Excel não salvo (instale openpyxl): {e}")

        print(f"\n💰 SUCESSO! {len(self.data)} itens extraídos.")
        print(f"📂 CSV salvo: {csv_path}")

if __name__ == "__main__":
    # URL de teste (Sandbox segura para scraping)
    TARGET_URL = "http://books.toscrape.com"
    
    scraper = SimpleScraper(TARGET_URL)
    scraper.run(pages=2) # Scrapeia 2 páginas para demonstração
