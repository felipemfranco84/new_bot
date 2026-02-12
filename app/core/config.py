import os

class Settings:
    PROJECT_NAME: str = "New_Bot_Cloud"
    # O nome deve ser EXATAMENTE BASE_URL (maiusculo)
    BASE_URL: str = "https://nys.x1.america.travian.com/"
    
    VILAS = [
        {"nome": "Obellyx (Capital)", "link": "dorf1.php"},
        {"nome": "Vila 2", "link": "dorf1.php?newdid=50350"}
    ]
    
    TIMEOUT: int = 20
    MIN_WAIT_LOOP: int = 600
    MAX_WAIT_LOOP: int = 900

settings = Settings()