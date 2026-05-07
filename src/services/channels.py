"""Сервис для работы с каналами."""

from typing import Callable, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_engine import get_session

from src.core.interfaces.channels import ChannelRepoBase
from src.core.schemas.channel import ChannelModel, DeleteChannelModel


class ChannelService:
    """Сервис для работы с каналами."""

    def __init__(
            self,
            channel_repo: ChannelRepoBase,
            session_manager: Callable[[], AsyncContextManager[AsyncSession]] = get_session,
        ) -> None:
        self._session_manager = session_manager
        self._channel_repo = channel_repo

    async def get_channels(self) -> list[ChannelModel]:
        """Получить список каналов."""
        async with self._session_manager() as session:
            return await self._channel_repo.get_channels(session)

    async def add_channel(self, channel: ChannelModel) -> None:
        """Добавить канал."""
        async with self._session_manager() as session:
            await self._channel_repo.add_channel(session, channel)

    async def delete_channel(self, delete_channel_model: DeleteChannelModel) -> None:
        """Удалить канал."""
        async with self._session_manager() as session:
            await self._channel_repo.delete_channel(session, delete_channel_model)
