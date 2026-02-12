import os

class Settings:
    PROJECT_NAME: str = "New_Bot_Cloud"
    BASE_URL: str = "https://nys.x1.america.travian.com/"
    
    # ADICIONE SEU USUARIO E SENHA AQUI
    USER: str = "felipemfranco@outlook.com"
    PASS: str = "SUA_SENHAQlydludg@1984"
    
    # Caminho fixo para salvar cookies na VM (dentro da pasta do bot)
    PROFILE_PATH: str = os.path.abspath("./app/core/user_data")
    
    VILAS = [
        {"nome": "Obellyx (Capital)", "link": "dorf1.php"},
        {"nome": "Vila 2", "link": "dorf1.php?newdid=50350"}
    ]
    
    TIMEOUT: int = 30
    MIN_WAIT_LOOP: int = 600
    MAX_WAIT_LOOP: int = 900

settings = Settings()