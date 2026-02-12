from app.services.browser import BrowserService
from app.core.config import settings
import logging, time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

def iniciar_bot():
    driver = BrowserService.obter_driver()
    try:
        for vila in settings.VILAS:
            logger.info(f"Navegando para {vila['nome']}")
            driver.get(settings.URL_BASE + vila['link'])
            
            # Aqui entra a lógica de Scraper -> Architect -> Action
            # que vamos plugar nos services
            time.sleep(5)
    finally:
        driver.quit()

if __name__ == "__main__":
    iniciar_bot()