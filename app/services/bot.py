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
        self.wait = WebDriverWait(self.driver, 10) # Timeout curto para evitar travamentos longos
        self.logger = logging.getLogger("New_Bot.Logic")
        self.mapa_gid = {"Madeira": "gid1", "Barro": "gid2", "Ferro": "gid3", "Trigo": "gid4"}

    def realizar_login(self, user, password):
        """Injeta credenciais via JS para ignorar lentidao grafica."""
        try:
            self.logger.info("Executando login via injeção direta de JS...")
            
            # Script para preencher e clicar sem esperar renderização
            script = f"""
                document.querySelector('input[name="name"]').value = '{user}';
                document.querySelector('input[name="password"]').value = '{password}';
                document.querySelector('button[type="submit"]').click();
            """
            self.driver.execute_script(script)
            
            # Espera 10s para o servidor processar o redirecionamento
            time.sleep(10)
            
            if "dorf1" in self.driver.current_url or self.driver.find_elements(By.ID, "l1"):
                self.logger.info("✅ Login confirmado via JS Injection.")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Falha na injecao de login: {e}")
            return False

    def obter_recursos(self):
        try:
            # Verifica apenas se os IDs basicos existem no HTML bruto
            elementos = self.driver.find_elements(By.ID, "l1")
            if not elementos:
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
        try:
            return len(self.driver.find_elements(By.CSS_SELECTOR, ".buildingList li, .constructionList li"))
        except:
            return 0

    def executar_construcao(self, recurso):
        try:
            obras_antes = self.contar_fila()
            gid = self.mapa_gid[recurso]
            
            # Clica via JS para evitar problemas de 'ElementNotClickable'
            campo = self.driver.find_element(By.CSS_SELECTOR, f".{gid}")
            self.driver.execute_script("arguments[0].click();", campo)
            
            time.sleep(5)
            
            # Clica no botao de evoluir via JS
            self.driver.execute_script("""
                let btn = Array.from(document.querySelectorAll('button')).find(b => 
                    b.innerText.includes('Melhorar') || 
                    b.innerText.includes('Evoluir') || 
                    b.innerText.includes('Construir')
                );
                if(btn) btn.click();
            """)
            
            time.sleep(5)
            self.driver.get(self.driver.current_url.split('?')[0])
            return self.contar_fila() > obras_antes
        except Exception as e:
            self.logger.error(f"Erro na execucao: {e}")
            return False