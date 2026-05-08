"""Телеграмм бот."""

from aiogram import Bot, Dispatcher

from src.core.interfaces.channels_service import ChannelServiceBase
from src.core.interfaces.messages_service import MessagesServiceBase

from src.bot.utils.middlewares import ContextMiddleware, AuthMiddleware

from src.bot.handlers import (
    common_router,
    messages_router,
    buttons_router,
    channels_router
)

class TelegramBot:
    """Телеграмм бот."""

    def __init__(
        self,
        token: str,
        allowed_users: list[int],
        channels_service: ChannelServiceBase,
        messages_service: MessagesServiceBase
    ) -> None:
        self._bot = Bot(token=token)
        self.dp = Dispatcher()
        self.allowed_users = allowed_users
        self.channels_service = channels_service
        self.messages_service = messages_service

    async def start(self) -> None:
        """Запустить бота."""
        for observer in [self.dp.message, self.dp.callback_query]:
            observer.middleware(AuthMiddleware(self.allowed_users))
            observer.middleware(
                ContextMiddleware(
                    self.channels_service,
                    self.messages_service
                )
            )

        self.dp.include_router(
            common_router,
            messages_router,
            buttons_router,
            channels_router,
        )

        await self.dp.start_polling(self._bot)
