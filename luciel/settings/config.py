from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Luciel"
    WEBHOOK_URL: str = "https://example.com/webhook"

    DATABASE_PATH: str = "./database/database.json"

    

settings = Settings()