import logging, time, random
from app.services.browser import BrowserService
from app.services.bot import BotService
from app.core.config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("New_Bot.Main")

def executar_ciclo():
    driver = BrowserService.obter_driver()
    bot = BotService(driver)
    
    try:
        for vila in settings.VILAS:
            logger.info(f"========== {vila['nome']} ==========")
            driver.get(settings.BASE_URL + vila['link'])
            
            recursos = bot.obter_recursos()
            if not recursos: continue
            
            if bot.contar_fila() >= 1:
                logger.info("Fila ocupada.")
            else:
                menor = min(recursos, key=recursos.get)
                logger.info(f"Prioridade: {menor} ({recursos[menor]})")
                if bot.executar_construcao(menor):
                    logger.info("✅ SUCESSO REAL.")
                else:
                    logger.warning("❌ FALHA OU BLOQUEIO.")
            
            time.sleep(random.randint(5, 10))
    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        try:
            executar_ciclo()
            espera = random.randint(settings.MIN_WAIT_LOOP, settings.MAX_WAIT_LOOP)
            logger.info(f"Aguardando {espera//60} minutos...")
            time.sleep(espera)
        except KeyboardInterrupt: break
        except Exception as e:
            logger.error(f"Erro no loop: {e}")
            time.sleep(60)