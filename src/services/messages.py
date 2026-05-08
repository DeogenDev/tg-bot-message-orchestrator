"""Сервис сообщений"""

from typing import Callable, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_engine import get_session

from src.core.interfaces.messages_service import MessagesServiceBase
from src.core.interfaces.messages import MessageRepoBase

from src.core.schemas.message import (
    MessageModel,
    ButtonModel,
    DeleteMessageModel,
    DeleteButtonModel
)


class MessagesService(MessagesServiceBase):
    """Сервис сообщений."""

    def __init__(
        self,
        messages_repo: MessageRepoBase,
        session_manager: Callable[[], AsyncContextManager[AsyncSession]] = get_session,
    ):
        self._messages_repo = messages_repo
        self._session_manager = session_manager

    async def get_messages(self) -> list[MessageModel]:
        """Получить список сообщений."""
        async with self._session_manager() as session:
            return await self._messages_repo.get_messages(session)

    async def add_message(self, message: MessageModel) -> None:
        """Добавить сообщение."""
        async with self._session_manager() as session:
            await self._messages_repo.add_message(session, message)

    async def edit_message(self, message: MessageModel) -> None:
        """Обновить только текст сообщения."""
        async with self._session_manager() as session:
            await self._messages_repo.edit_message(session, message)

    async def add_button(self, button: ButtonModel) -> None:
        """Добавить кнопку."""
        async with self._session_manager() as session:
            await self._messages_repo.add_button(session, button)

    async def delete_message(self, delete_message_model: DeleteMessageModel) -> None:
        """Удалить сообщение."""
        async with self._session_manager() as session:
            await self._messages_repo.delete_message(session, delete_message_model)

    async def delete_button(self, delete_button_model: DeleteButtonModel) -> None:
        """Удалить кнопку."""
        async with self._session_manager() as session:
            await self._messages_repo.delete_button(session, delete_button_model)
