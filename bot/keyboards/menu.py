from aiogram.types import MenuButtonWebApp, WebAppInfo


def get_webapp_menu(webapp: WebAppInfo) -> MenuButtonWebApp:
    """Создает меню с веб-приложением

    Args:
        webapp (WebAppInfo): информация о веб-приложении

    Returns:
        MenuButtonWebApp: меню с веб-приложением
    """
    return MenuButtonWebApp(text="Конструктор", web_app=webapp)
