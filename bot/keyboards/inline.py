from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def get_webapp_inline_kb(webapp: WebAppInfo) -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру с веб-приложением

    Args:
        webapp (WebAppInfo): информация о веб-приложении

    Returns:
        InlineKeyboardMarkup: инлайн-клавиатура с веб-приложением
    """

    buttons = [
        [InlineKeyboardButton(text="Открыть конструктор", web_app=webapp)],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return markup
