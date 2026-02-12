import undetected_chromedriver as uc
import logging

logger = logging.getLogger("New_Bot.Browser")

class BrowserService:
    @staticmethod
    def obter_driver():
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Headless=new é o padrão moderno que não é detectado facilmente
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        
        try:
            # O UC baixa o driver automaticamente compatível com o Chrome da VM
            driver = uc.Chrome(options=options)
            # Stealth extra: Remove rastros de automação via JS
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Motor Desktop UC iniciado com sucesso.")
            return driver
        except Exception as e:
            logger.error(f"Erro ao iniciar Undetected-Chromedriver: {e}")
            raise