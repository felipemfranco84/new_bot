import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BotService:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    def esperar_e_clicar(self, xpath):
        elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        time.sleep(1) # Delay humano
        elemento.click()

    def ler_recursos(self):
        # Espera o recurso carregar em vez de sleep fixo
        self.wait.until(EC.presence_of_element_located((By.ID, "l1")))
        # ... lógica de extração (idêntica à anterior)