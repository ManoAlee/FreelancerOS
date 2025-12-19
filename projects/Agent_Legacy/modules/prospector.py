import time
import logging
import random

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🕷️ MÓDULO: PROSPECTOR (OLHEIRO)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Objetivo: Varrer o Freelancer.com (Simulado) e achar jobs.
# Filtra por ROI: Só traz o que paga bem e é rápido.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from selenium.webdriver.common.by import By

class MarketScanner:
    def __init__(self, keywords, driver=None):
        self.keywords = keywords
        self.driver = driver # Recebe o navegador real
        self.logger = logging.getLogger('MarketScanner')

    def scan_opportunities(self):
        """
        Varre o Freelancer.com usando Selenium.
        """
        if not self.driver:
            print("   ⚠️ [SCANNER] Modo Simulação (Sem Browser).")
            return self._mock_scan()

        print(f"\n🔎 [SCANNER] Buscando projetos reais para: {self.keywords}...")
        
        # URL de busca de projetos (Ajuste conforme a URL real de busca)
        # Exemplo: https://www.freelancer.com/jobs/python_script/
        search_query = self.keywords[0].replace(" ", "-")
        url = f"https://www.freelancer.com/jobs/{search_query}/"
        
        self.driver.get(url)
        time.sleep(3) # Espera carregar lista
        
        found_jobs = []
        
        try:
            # Seletores CSS precisam ser atualizados conforme o site muda
            # Aqui usamos seletores genéricos de exemplo baseados na estrutura comum
            project_cards = self.driver.find_elements(By.CSS_SELECTOR, ".JobSearchCard-item")
            
            for card in project_cards[:5]: # Pega os top 5
                try:
                    title = card.find_element(By.CSS_SELECTOR, ".JobSearchCard-primary-heading-link").text
                    desc = card.find_element(By.CSS_SELECTOR, ".JobSearchCard-primary-description").text
                    budget_text = card.find_element(By.CSS_SELECTOR, ".JobSearchCard-secondary-price").text
                    
                    # Limpeza básica do budget
                    budget = 0
                    if "$" in budget_text:
                        budget = int(budget_text.split("$")[1].split(" ")[0].replace(",", ""))
                    
                    found_jobs.append({
                        "title": title,
                        "description": desc,
                        "budget": budget,
                        "client_verified": True # Assumindo true para teste
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"   ⚠️ Erro ao ler HTML: {e}")
            return self._mock_scan() # Fallback para mock se falhar

        print(f"   ✅ Encontradas {len(found_jobs)} oportunidades REAIS.")
        return found_jobs

    def _mock_scan(self):
        # ... (Código antigo de simulação mantido como backup)
        time.sleep(2)
        return [
            {
                "id": 101,
                "title": "Need Python Script to Scrape Emails",
                "budget": 50,
                "description": "I need a simple script to get emails from a list of websites.",
                "client_verified": True
            }
        ]
