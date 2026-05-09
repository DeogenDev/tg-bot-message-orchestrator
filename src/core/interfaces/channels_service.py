"""Интерфейс сервиса каналов."""

from abc import ABC, abstractmethod

from src.core.schemas.channel import ChannelModel, DeleteChannelModel


class ChannelServiceBase(ABC):
    """Интерфейс сервиса каналов."""

    @abstractmethod
    async def get_channels(self) -> list[ChannelModel]:
        """Получить список каналов."""
        raise NotImplementedError

    @abstractmethod
    async def add_channel(self, channel: ChannelModel) -> None:
        """Добавить канал."""
        raise NotImplementedError

    @abstractmethod
    async def delete_channel(self, delete_channel_model: DeleteChannelModel) -> None:
        """Удалить канал."""
        raise NotImplementedError

