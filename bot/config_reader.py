from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_TOKEN: SecretStr
    MODE: str
    SERVER_NAME: str


config = Settings()
