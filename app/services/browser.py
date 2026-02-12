import undetected_chromedriver as uc
import logging
from app.core.config import settings

logger = logging.getLogger("New_Bot.Browser")

class BrowserService:
    @staticmethod
    def obter_driver():
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-data-dir={settings.PROFILE_PATH}")
        
        # Removemos o page_load_strategy eager para garantir estabilidade do JS
        options.add_argument("--disable-gpu")
        options.add_argument("--blink-settings=imagesEnabled=false") # Mantem sem imagens

        try:
            driver = uc.Chrome(options=options)
            driver.set_page_load_timeout(30)
            return driver
        except Exception as e:
            logger.error(f"Erro no motor: {e}")
            raise