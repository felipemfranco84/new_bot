import undetected_chromedriver as uc
import logging

logger = logging.getLogger("New_Bot.Browser")

class BrowserService:
    @staticmethod
    def obter_driver():
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        
        # Flags para evitar que o processo trave em servidores
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        
        try:
            driver = uc.Chrome(options=options)
            driver.set_page_load_timeout(30) # Timeout de 30s
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Motor Desktop UC iniciado e otimizado para Cloud.")
            return driver
        except Exception as e:
            logger.error(f"Erro ao iniciar Undetected-Chromedriver: {e}")
            raise