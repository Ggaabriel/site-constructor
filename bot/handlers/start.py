import httpx
from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config_reader import config
from keyboards import get_webapp_inline_kb, get_webapp_menu
from utils import get_webapp

router = Router()


@router.message(CommandStart())
async def start(message: Message, bot: Bot) -> None:
    """Обрабатывает команду /start

    Args:
        message (Message): Сообщение
        bot (Bot): Бот
    """
    async with httpx.AsyncClient() as client:
        url = f"{config.SERVER_NAME}/api/v1/users/"
        _id = str(message.from_user.id if message.from_user is not None else 0)

        response = await client.post(
            url=url,
            json={"id": _id},
        )

    match response.status_code:
        case 201:
            text = (
                "Добро пожаловать в бот-конструктор сайтов.\n"
                "Начните создание сайта по кнопке ниже."
            )
        case 409:
            text = "Вы уже зарегистрированы. Начните создание сайта по кнопке ниже."
        case _:
            text = "Произошла ошибка. Начните создание сайта по кнопке ниже."

    webapp = get_webapp()

    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=get_webapp_menu(webapp),
    )

    await message.answer(
        text=text,
        reply_markup=get_webapp_inline_kb(webapp),
    )
