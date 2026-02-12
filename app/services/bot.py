import logging, time, re, random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BotService:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.logger = logging.getLogger("New_Bot.Logic")
        self.mapa_gid = {"Madeira": "gid1", "Barro": "gid2", "Ferro": "gid3", "Trigo": "gid4"}

    def obter_recursos(self):
        """Lê recursos usando esperas inteligentes."""
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "l1")))
            recursos = {}
            mapa_nomes = {1: "Madeira", 2: "Barro", 3: "Ferro", 4: "Trigo"}
            for i in range(1, 5):
                texto = self.driver.find_element(By.ID, f"l{i}").text
                recursos[mapa_nomes[i]] = int(re.sub(r'\D', '', texto))
            return recursos
        except Exception as e:
            self.logger.error(f"Falha na leitura: {e}")
            return None

    def contar_fila(self):
        """Conta obras reais na fila."""
        for seletor in [".buildingList li", ".constructionList li"]:
            itens = self.driver.find_elements(By.CSS_SELECTOR, seletor)
            if itens: return len(itens)
        return 0

    def executar_construcao(self, recurso):
        """Fluxo de clique e validação real."""
        try:
            obras_antes = self.contar_fila()
            gid = self.mapa_gid[recurso]
            
            # Clica no campo (ex: .gid4 para trigo)
            campo = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".{gid}")))
            self.driver.execute_script("arguments[0].click();", campo)
            
            # Busca botão por texto (Melhorar/Evoluir/Construir)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(random.uniform(2, 4))
            
            botoes = self.driver.find_elements(By.XPATH, "//button[contains(., 'Melhorar') or contains(., 'Evoluir') or contains(., 'Construir')]")
            
            if botoes:
                self.driver.execute_script("arguments[0].click();", botoes[0])
                self.logger.info(f"Clique enviado para {recurso}.")
                time.sleep(5)
                # Volta para validar
                self.driver.get(self.driver.current_url.split('?')[0])
                if self.contar_fila() > obras_antes:
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Erro na acao: {e}")
            return False