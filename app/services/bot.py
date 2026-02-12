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
        self.wait = WebDriverWait(self.driver, 25)
        self.logger = logging.getLogger("New_Bot.Logic")
        self.mapa_gid = {"Madeira": "gid1", "Barro": "gid2", "Ferro": "gid3", "Trigo": "gid4"}

    def realizar_login(self, user, password):
        """Tenta logar usando seletores de tipo (mais estaveis)."""
        try:
            self.logger.info("Iniciando tentativa de login Desktop...")
            
            # Busca campos por atributo TYPE (universal no Travian)
            user_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text'], input[name='name']")))
            pass_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
            
            # Limpa e digita com delay humano
            user_field.click()
            user_field.clear()
            for char in user:
                user_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            pass_field.click()
            pass_field.clear()
            for char in password:
                pass_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(1)
            
            # Busca o botao verde (Login)
            btn_xpath = "//button[contains(@class, 'green')] | //button[@type='submit']"
            login_btn = self.driver.find_element(By.XPATH, btn_xpath)
            self.driver.execute_script("arguments[0].click();", login_btn)
            
            # Espera carregar a aldeia (elemento l1)
            self.wait.until(EC.presence_of_element_located((By.ID, "l1")))
            self.logger.info("✅ Login confirmado e redirecionado para dorf1.")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro no processo de login: {e}")
            # Tira print do erro de login para vermos o que preencheu
            self.driver.save_screenshot("logs/FALHA_LOGIN.png")
            return False

    def obter_recursos(self):
        try:
            # Verifica se o elemento de recursos existe
            if not self.driver.find_elements(By.ID, "l1"):
                return None
            
            recursos = {}
            mapa_nomes = {1: "Madeira", 2: "Barro", 3: "Ferro", 4: "Trigo"}
            for i in range(1, 5):
                texto = self.driver.find_element(By.ID, f"l{i}").text
                recursos[mapa_nomes[i]] = int(re.sub(r'\D', '', texto))
            return recursos
        except Exception:
            return None

    def contar_fila(self):
        for seletor in [".buildingList li", ".constructionList li"]:
            itens = self.driver.find_elements(By.CSS_SELECTOR, seletor)
            if itens: return len(itens)
        return 0

    def executar_construcao(self, recurso):
        try:
            obras_antes = self.contar_fila()
            gid = self.mapa_gid[recurso]
            campo = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".{gid}")))
            self.driver.execute_script("arguments[0].click();", campo)
            
            time.sleep(random.uniform(2, 4))
            xpath_btn = "//button[contains(., 'Melhorar') or contains(., 'Evoluir') or contains(., 'Construir')]"
            botoes = self.driver.find_elements(By.XPATH, xpath_btn)
            
            if botoes:
                self.driver.execute_script("arguments[0].click();", botoes[0])
                time.sleep(5)
                self.driver.get(self.driver.current_url.split('?')[0])
                return self.contar_fila() > obras_antes
            return False
        except Exception as e:
            self.logger.error(f"Erro na execucao: {e}")
            return False