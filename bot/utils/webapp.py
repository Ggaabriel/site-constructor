from aiogram.types import WebAppInfo

from config_reader import config


def get_webapp() -> WebAppInfo:
    return WebAppInfo(url=f"{config.SERVER_NAME}")
