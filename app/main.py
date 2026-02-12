import logging
import time
import random
import sys
from app.services.browser import BrowserService
from app.services.bot import BotService
from app.core.config import settings

# Configuração de Logs otimizada para monitoramento via SSH na VM
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("New_Bot.Main")

def executar_ciclo():
    """Realiza uma varredura completa nas aldeias configuradas."""
    driver = None
    try:
        driver = BrowserService.obter_driver()
        bot = BotService(driver)
        
        for vila in settings.VILAS:
            logger.info(f"========== TRABALHANDO EM: {vila['nome']} ==========")
            
            # Navegação usando a constante corrigida BASE_URL
            url_alvo = settings.BASE_URL + vila['link']
            driver.get(url_alvo)
            
            # Espera inteligente (definida dentro do bot.obter_recursos)
            recursos = bot.obter_recursos()
            if not recursos:
                logger.error(f"[{vila['nome']}] Nao foi possivel ler os recursos. Pulando...")
                continue
            
            logger.info(f"[{vila['nome']}] Recursos: {recursos}")
            
            # Verifica fila de construcao
            obras_atuais = bot.contar_fila()
            
            if obras_atuais >= 1:
                logger.info(f"[{vila['nome']}] Fila ja possui {obras_atuais} obra(s). Ocupada.")
            else:
                # Decisão baseada no menor recurso (Architect logic embutida no BotService)
                menor_recurso = min(recursos, key=recursos.get)
                logger.info(f"[{vila['nome']}] Prioridade detectada: {menor_recurso}")
                
                # Execução com validação real (Actions logic)
                sucesso = bot.executar_construcao(menor_recurso)
                
                if sucesso:
                    logger.info(f"[{vila['nome']}] ✅ SUCESSO REAL: Obra iniciada e confirmada.")
                else:
                    logger.warning(f"[{vila['nome']}] ❌ FALHA: Acao tentada, mas nao confirmada na fila.")
            
            # Intervalo entre aldeias para mimetismo humano
            time.sleep(random.randint(5, 12))

    except Exception as e:
        logger.error(f"Erro critico durante o ciclo: {e}")
    finally:
        if driver:
            driver.quit()
            logger.info("Navegador encerrado. Ciclo de vilas finalizado.")

if __name__ == "__main__":
    logger.info(f"=== {settings.PROJECT_NAME} v1.0.3 ATIVADO ===")
    
    while True:
        try:
            executar_ciclo()
            
            # Espera aleatória entre os ciclos (definida no config.py)
            segundos_espera = random.randint(settings.MIN_WAIT_LOOP, settings.MAX_WAIT_LOOP)
            proxima_rodada = time.strftime('%H:%M:%S', time.localtime(time.time() + segundos_espera))
            
            logger.info(f"DORMINDO: Proxima varredura programada para as {proxima_rodada}.")
            time.sleep(segundos_espera)
            
        except KeyboardInterrupt:
            logger.info("Bot interrompido manualmente pelo usuario.")
            break
        except Exception as e:
            logger.error(f"Erro no loop de espera: {e}")
            time.sleep(60