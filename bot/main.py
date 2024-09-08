import json
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types.update import Update

from config_reader import config
from handlers import setup_message_routers

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
bot = Bot(config.TELEGRAM_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)

dp = Dispatcher()
message_routers = setup_message_routers()
dp.include_router(message_routers)


async def handler(event: dict, _: dict) -> dict:
    body = json.loads(event["body"])
    update_id = body["update_id"]
    message = body["message"]

    update = Update(update_id=update_id, message=message)

    await dp.feed_update(bot=bot, update=update)

    return {"statusCode": 200, "body": "ok"}
