import os

class Settings:
    PROJECT_NAME: str = "New_Bot_Cloud"
    # No Ubuntu, o Chrome costuma ficar aqui
    CHROME_PATH: str = "/usr/bin/google-chrome"
    URL_BASE: str = "https://nys.x1.america.travian.com/"
    VILAS = [
        {"nome": "Obellyx (Capital)", "link": "dorf1.php"},
        {"nome": "Vila 2", "link": "dorf1.php?newdid=50350"}
    ]
    TIMEOUT: int = 20

settings = Settings()