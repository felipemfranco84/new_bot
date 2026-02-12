import logging
import time
import random
import sys
import os
from app.services.browser import BrowserService
from app.services.bot import BotService
from app.core.config import settings

# Garante que a pasta de logs existe
os.makedirs("logs", exist_ok=True)

# Configuracao de Log Duplo (Terminal + Arquivo)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/execucao.log", encoding='utf-8')
    ]
)
logger = logging.getLogger("New_Bot.Main")

def executar_ciclo():
    driver = None
    try:
        driver = BrowserService.obter_driver()
        bot = BotService(driver)
        
        for vila in settings.VILAS:
            logger.info(f">>> ALDEIA ATUAL: {vila['nome']}")
            url = settings.BASE_URL + vila['link']
            
            try:
                logger.info(f"Navegando para: {url}")
                driver.get(url)
                
                # Screenshot de Seguranca (Ver o que carregou)
                driver.save_screenshot(f"logs/last_page_{vila['nome'].replace(' ', '_')}.png")
                logger.info(f"Pagina carregada. Foto salva em logs/last_page...")

                recursos = bot.obter_recursos()
                if not recursos:
                    logger.warning("Nao consegui ler recursos. O Chrome pode estar em branco.")
                    continue
                
                logger.info(f"Recursos lidos: {recursos}")
                
                obras = bot.contar_fila()
                logger.info(f"Obras na fila: {obras}")

                if obras < 1:
                    menor = min(recursos, key=recursos.get)
                    logger.info(f"Tentando evoluir: {menor}")
                    bot.executar_construcao(menor)
                
            except Exception as e:
                logger.error(f"Erro durante interacao na vila {vila['nome']}: {e}")
                driver.save_screenshot(f"logs/ERRO_{vila['nome'].replace(' ', '_')}.png")
            
            time.sleep(random.randint(5, 10))

    except Exception as e:
        logger.error(f"ERRO CRITICO NO MOTOR: {e}")
        if driver: driver.save_screenshot("logs/CRITICAL_FAIL.png")
    finally:
        if driver:
            driver.quit()
            logger.info("Ciclo finalizado. Driver encerrado.")

if __name__ == "__main__":
    logger.info("=== INICIANDO SISTEMA DE DIAGNOSTICO v1.1.0 ===")
    executar_ciclo()