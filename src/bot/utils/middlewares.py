"""Мидлвары бота."""

from typing import Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.core.interfaces.channels_service import ChannelServiceBase
from src.core.interfaces.messages_service import MessagesServiceBase

from .texts import texts


class ContextMiddleware(BaseMiddleware):
    """Мидлвар для передачи контекста в хендлеры."""

    def __init__(
        self,
        channel_service: ChannelServiceBase,
        messages_service: MessagesServiceBase,
    ):
        """Инициализация мидлвара."""
        self.channel_service = channel_service
        self.messages_service = messages_service


    async def __call__(self, handler, event, data):
        """Внедрение сервисов и текстов."""
        data["channel_service"] = self.channel_service
        data["messages_service"] = self.messages_service
        data["texts"] = texts
        return await handler(event, data)


class AuthMiddleware(BaseMiddleware):
    """Мидлвар для проверки авторизации."""

    def __init__(
        self,
        allowed_users: list[int],
    ):
        """Инициализация мидлвара."""
        self.allowed_users = allowed_users

    async def __call__(
        self,
        handler,
        event: Union[Message, CallbackQuery],
        data: dict,
    ) -> None:
        """Внедрение сервисов и текстов."""
        user_id = event.from_user.id
        if user_id not in self.allowed_users:
            return
        return await handler(event, data)
