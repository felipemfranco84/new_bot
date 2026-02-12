import undetected_chromedriver as uc
from app.core.config import settings
import os

# Garante a pasta de logs
os.makedirs("logs", exist_ok=True)

options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument(f"--user-data-dir={settings.PROFILE_PATH}")

print("Iniciando Chrome para captura...")
driver = uc.Chrome(options=options)
try:
    driver.get(settings.BASE_URL + "dorf1.php")
    # Espera um pouco para carregar
    import time
    time.sleep(5)
    
    caminho = "logs/print_manual.png"
    driver.save_screenshot(caminho)
    print(f"✅ Screenshot salva com sucesso em: {caminho}")
finally:
    driver.quit()