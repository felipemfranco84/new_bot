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
        
        # O SEGREDOS PARA CLOUD:
        options.page_load_strategy = 'eager' # Interage antes de carregar imagens/scripts
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--blink-settings=imagesEnabled=false") # Desativa imagens

        try:
            driver = uc.Chrome(options=options)
            driver.set_page_load_timeout(settings.TIMEOUT)
            driver.set_script_timeout(settings.TIMEOUT)
            return driver
        except Exception as e:
            logger.error(f"Erro ao iniciar Chrome: {e}")
            raise