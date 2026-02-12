import undetected_chromedriver as uc
from app.core.config import settings
import os
import time

# Garante a pasta de logs
os.makedirs("logs", exist_ok=True)

options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# IMPORTANTE: Remova temporariamente o user-data-dir para testar se o Chrome abre puro
# options.add_argument(f"--user-data-dir={settings.PROFILE_PATH}") 

print("🚀 Iniciando Chrome via VENV...")
try:
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.get(settings.BASE_URL + "dorf1.php")
    time.sleep(10)
    
    driver.save_screenshot("logs/print_limpo.png")
    print("✅ Print salvo em logs/print_limpo.png")
    driver.quit()
except Exception as e:
    print(f"❌ Erro ao abrir: {e}")