import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🖥️ MÓDULO: BROWSER DRIVER (SELENIUM REAL)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Controla o Chrome real para logar e navegar.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BrowserDriver:
    def __init__(self, headless=False):
        self.logger = logging.getLogger('BrowserDriver')
        self.driver = self._setup_driver(headless)

    def _setup_driver(self, headless):
        """Configura o Chrome com opções anti-detecção básicas."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        # User-Agent comum para parecer humano
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def login_freelancer(self, username, password):
        """Faz login no Freelancer.com."""
        print("   🔑 [BROWSER] Acessando página de login...")
        self.driver.get("https://www.freelancer.com/login")
        
        try:
            # Espera campo de email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username")) # ID pode variar, ajustar se necessário
            )
            email_field.clear()
            email_field.send_keys(username)
            time.sleep(1)

            # Espera campo de senha
            pass_field = self.driver.find_element(By.ID, "password") # ID pode variar
            pass_field.clear()
            pass_field.send_keys(password)
            time.sleep(1)

            # Clica no botão de login
            login_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_btn.click()
            
            print("   ⏳ [BROWSER] Aguardando redirecionamento...")
            time.sleep(5) # Espera carregar dashboard
            
            if "login" not in self.driver.current_url:
                print("   ✅ [BROWSER] Login realizado com sucesso!")
                return True
            else:
                print("   ❌ [BROWSER] Falha no login. Verifique credenciais.")
                return False

        except Exception as e:
            print(f"   ❌ [BROWSER] Erro no login: {e}")
            return False

    def close(self):
        self.driver.quit()
