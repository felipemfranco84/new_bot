import undetected_chromedriver as uc
import logging
from app.core.config import settings

logger = logging.getLogger("New_Bot.Browser")

class BrowserService:
    @staticmethod
    def obter_driver():
        options = uc.ChromeOptions()
        # Removendo sandbox apenas se necessario, mantendo foco em ser indetectavel
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-data-dir={settings.PROFILE_PATH}")
        
        # Flags para evitar o travamento do renderizador no Ubuntu
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-infobars")
        options.add_argument("--force-device-scale-factor=1")

        try:
            # UC cuida do bypass de automacao nativamente
            driver = uc.Chrome(options=options, use_subprocess=True)
            driver.set_page_load_timeout(60) 
            return driver
        except Exception as e:
            logger.error(f"Erro no motor UC: {e}")
            raise