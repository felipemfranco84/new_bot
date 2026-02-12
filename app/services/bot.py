import logging
import time
import re
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BotService:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        self.logger = logging.getLogger("New_Bot.Logic")
        self.mapa_gid = {"Madeira": "gid1", "Barro": "gid2", "Ferro": "gid3", "Trigo": "gid4"}

    def realizar_login(self, user, password):
        """Para o carregamento infinito e tenta autenticacao."""
        try:
            self.logger.info("Interrompendo scripts pesados para liberar o login...")
            # Forca o navegador a parar de carregar 'lixo' visual que causa o timeout
            self.driver.execute_script("window.stop();")
            
            time.sleep(2)
            
            # Busca os campos usando seletores múltiplos (fallback)
            user_input = self.wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "input[name='name'], input[type='text']"
            )))
            pass_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']")
            
            self.logger.info("Preenchendo campos...")
            user_input.clear()
            user_input.send_keys(user)
            time.sleep(0.5)
            pass_input.clear()
            pass_input.send_keys(password)
            
            # Tenta clicar no botao de login via JS para evitar interceptacao
            self.driver.execute_script("""
                let btn = document.querySelector('button[type="submit"]') || document.querySelector('button.green');
                if(btn) btn.click();
            """)
            
            # Aguarda o elemento l1 (sucesso) ou dorf1 na URL
            time.sleep(10)
            if "dorf1" in self.driver.current_url or len(self.driver.find_elements(By.ID, "l1")) > 0:
                self.logger.info("✅ Autenticacao bem sucedida.")
                return True
            
            self.driver.save_screenshot("logs/FALHA_APOS_CLIQUE.png")
            return False
        except Exception as e:
            self.logger.error(f"Erro durante o fluxo de login: {e}")
            return False

    def obter_recursos(self):
        try:
            # Sem esperar infinitamente, apenas checa se existe
            recursos_ids = ["l1", "l2", "l3", "l4"]
            if not all(self.driver.find_elements(By.ID, rid) for rid in recursos_ids):
                return None
            
            recursos = {}
            mapa_nomes = {1: "Madeira", 2: "Barro", 3: "Ferro", 4: "Trigo"}
            for i in range(1, 5):
                texto = self.driver.find_element(By.ID, f"l{i}").text
                recursos[mapa_nomes[i]] = int(re.sub(r'\D', '', texto))
            return recursos
        except:
            return None

    def contar_fila(self):
        try:
            return len(self.driver.find_elements(By.CSS_SELECTOR, ".buildingList li, .constructionList li"))
        except:
            return 0

    def executar_construcao(self, recurso):
        # ... (Logica de construcao mantida como v1.2.4)
        return False