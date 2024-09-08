from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    """Мидлварь для ограничения количества вызовов хендлера"""

    def __init__(self, time_limit: int | float = 2) -> None:
        """Создает экземпляр ThrottlingMiddleware

        Args:
            time_limit (int | float, optional): Задержка, при срабатывании\
            "отключает" хендлер на определенное время.
            По умолчанию 1 секунда.
        """
        self._limit: TTLCache = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not (isinstance(event, Message) or isinstance(event, CallbackQuery)):
            return
        id = event.from_user.id if event.from_user else 0
        if id in self._limit:
            return
        else:
            self._limit[id] = None
        return await handler(event, data)
