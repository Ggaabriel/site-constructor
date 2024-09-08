from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    mode: str = "local"
    server_name: str = "http://localhost"
    bot_key: str = ""
    storage: str = "/storage"
    max_file_size: int = 2097152


settings = Setting()
