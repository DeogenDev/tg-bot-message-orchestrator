"""Интерфейс для управления каналами."""

from abc import ABC, abstractmethod

from src.core.schemas.channel import Channel, DeleteChannel


class ChannelRepoBase(ABC):
    """Интерфейс для управления каналами."""

    @abstractmethod
    def add_channel(self, channel: Channel) -> None:
        """Добавить канал."""
        raise NotImplementedError

    @abstractmethod
    def get_channels(self) -> list[Channel]:
        """Получить список каналов."""
        raise NotImplementedError

    @abstractmethod
    def delete_channel(self, delete_channel_model: DeleteChannel) -> None:
        """Удалить канал."""
        raise NotImplementedError
