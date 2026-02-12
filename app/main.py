import logging
import time
import random
import sys
import os
from app.services.browser import BrowserService
from app.services.bot import BotService
from app.core.config import settings

# Garante pasta de logs e persistencia
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
            driver.get(url_alvo)
            
            # CHECAGEM DE LOGIN: Se nao vir os recursos, tenta logar
            if not bot.obter_recursos():
                if "login.php" in driver.current_url or driver.find_elements(By.NAME, "password"):
                    if not bot.realizar_login(settings.USER, settings.PASS):
                        logger.error("Falha no login. Abortando vila.")
                        continue
                else:
                    logger.error("Nao foi possivel carregar a vila.")
                    continue
            
            recursos = bot.obter_recursos()
            logger.info(f"Recursos: {recursos}")
            
            if bot.contar_fila() >= 1:
                logger.info("Fila ocupada.")
            else:
                menor = min(recursos, key=recursos.get)
                logger.info(f"Prioridade: {menor}")
                if bot.executar_construcao(menor):
                    logger.info("✅ SUCESSO CONFIRMADO.")
                else:
                    logger.warning("❌ FALHA NA ACAO.")
            
            time.sleep(random.randint(5, 12))

    except Exception as e:
        logger.error(f"Erro critico no ciclo: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logger.info(f"=== {settings.PROJECT_NAME} v1.2.1 INICIADO ===")
    while True:
        try:
            executar_ciclo()
            espera = random.randint(settings.MIN_WAIT_LOOP, settings.MAX_WAIT_LOOP)
            logger.info(f"DORMINDO: {espera//60} minutos.")
            time.sleep(espera)
        except KeyboardInterrupt: break
        except Exception: time.sleep(60)