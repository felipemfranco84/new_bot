import undetected_chromedriver as uc
import logging
import os

logger = logging.getLogger("New_Bot.Browser")

class BrowserService:
    @staticmethod
    def obter_driver():
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        
        # Flags de estabilidade para evitar travamento em VM
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--remote-debugging-port=9222") 

        try:
            logger.info("Iniciando instancia do Chrome...")
            driver = uc.Chrome(options=options)
            driver.set_page_load_timeout(45) # Timeout estendido
            logger.info("Chrome iniciado. Removendo rastro de automacao...")
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            logger.error(f"FALHA NO MOTOR: {e}")
            raise