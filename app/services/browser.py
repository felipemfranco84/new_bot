import undetected_chromedriver as uc
import logging

logger = logging.getLogger("New_Bot.Browser")

class BrowserService:
    @staticmethod
    def obter_driver():
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Recomendado iniciar visível na VM para testar, depois headless=new
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080") # Resolução Desktop
        
        try:
            driver = uc.Chrome(options=options)
            # Remove flag de automação
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            logger.error(f"Falha ao iniciar UC: {e}")
            raise