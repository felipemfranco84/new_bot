import logging
import time
import random
import sys
import os
from app.services.browser import BrowserService
from app.services.bot import BotService
from app.core.config import settings

os.makedirs("logs", exist_ok=True)
os.makedirs(settings.PROFILE_PATH, exist_ok=True)

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("logs/execucao.log")]
)
logger = logging.getLogger("New_Bot.Main")

def executar_ciclo():
    driver = None
    try:
        driver = BrowserService.obter_driver()
        bot = BotService(driver)
        
        for vila in settings.VILAS:
            logger.info(f"========== {vila['nome']} ==========")
            url_alvo = settings.BASE_URL + vila['link']
            
            try:
                driver.get(url_alvo)
                # Tira print imediatamente para debug se houver timeout parcial
                driver.save_screenshot(f"logs/debug_{vila['nome'].replace(' ', '_')}.png")
            except Exception as e:
                logger.warning(f"Timeout no get, tentando prosseguir: {e}")
                driver.save_screenshot("logs/timeout_debug.png")

            # Checagem de Login
            if not bot.obter_recursos():
                if "login" in driver.current_url or len(driver.find_elements("name", "password")) > 0:
                    if not bot.realizar_login(settings.USER, settings.PASS):
                        logger.error("Falha no login.")
                        continue
                else:
                    logger.error("Vila nao carregou corretamente.")
                    continue
            
            recursos = bot.obter_recursos()
            logger.info(f"Recursos: {recursos}")
            
            if bot.contar_fila() >= 1:
                logger.info("Fila ocupada.")
            else:
                menor = min(recursos, key=recursos.get)
                if bot.executar_construcao(menor):
                    logger.info("✅ SUCESSO.")
                else:
                    logger.warning("❌ FALHA.")
            
            time.sleep(random.randint(5, 10))

    except Exception as e:
        logger.error(f"Erro critico no ciclo: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logger.info(f"=== {settings.PROJECT_NAME} v1.2.2 ATIVADO ===")
    while True:
        try:
            executar_ciclo()
            espera = random.randint(settings.MIN_WAIT_LOOP, settings.MAX_WAIT_LOOP)
            logger.info(f"DORMINDO: {espera//60} minutos.")
            time.sleep(espera)
        except KeyboardInterrupt: break
        except Exception: time.sleep(60)