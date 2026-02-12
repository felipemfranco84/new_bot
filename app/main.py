import logging
import time
import random
import sys
from app.services.browser import BrowserService
from app.services.bot import BotService
from app.core.config import settings

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("New_Bot.Main")

def executar_ciclo():
    driver = None
    try:
        driver = BrowserService.obter_driver()
        bot = BotService(driver)
        
        for vila in settings.VILAS:
            logger.info(f"========== {vila['nome']} ==========")
            
            # Acesso direto ao atributo BASE_URL
            url_alvo = settings.BASE_URL + vila['link']
            driver.get(url_alvo)
            
            recursos = bot.obter_recursos()
            if not recursos:
                logger.error(f"[{vila['nome']}] Falha na leitura.")
                continue
            
            logger.info(f"[{vila['nome']}] Recursos: {recursos}")
            
            if bot.contar_fila() >= 1:
                logger.info(f"[{vila['nome']}] Fila ocupada.")
            else:
                menor_recurso = min(recursos, key=recursos.get)
                logger.info(f"[{vila['nome']}] Prioridade: {menor_recurso}")
                
                if bot.executar_construcao(menor_recurso):
                    logger.info(f"[{vila['nome']}] ✅ SUCESSO REAL.")
                else:
                    logger.warning(f"[{vila['nome']}] ❌ FALHA REAL.")
            
            time.sleep(random.randint(5, 12))

    except Exception as e:
        logger.error(f"Erro critico: {e}")
    finally:
        if driver:
            driver.quit()
            logger.info("Navegador encerrado.")

if __name__ == "__main__":
    logger.info(f"=== {settings.PROJECT_NAME} v1.0.4 ATIVADO ===")
    while True:
        try:
            executar_ciclo()
            espera = random.randint(settings.MIN_WAIT_LOOP, settings.MAX_WAIT_LOOP)
            logger.info(f"DORMINDO: {espera//60} minutos.")
            time.sleep(espera)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"Erro no loop: {e}")
            time.sleep(60)