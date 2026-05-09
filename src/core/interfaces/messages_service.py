"""Интерфейс сервиса сообщений."""

from abc import ABC, abstractmethod

from src.core.schemas.message import (
    MessageModel,
    ButtonModel,
    DeleteMessageModel,
    DeleteButtonModel
)

class MessagesServiceBase(ABC):
    """Интерфейс сервиса сообщений."""


    @abstractmethod
    async def get_messages(self) -> list[MessageModel]:
        """Получить список сообщений."""
        raise NotImplementedError

    @abstractmethod
    async def add_message(self, message: MessageModel) -> None:
        """Добавить сообщение."""
        raise NotImplementedError

    @abstractmethod
    async def edit_message(self, message: MessageModel) -> None:
        """Обновить только текст сообщения."""
        raise NotImplementedError

    @abstractmethod
    async def add_button(self, button: ButtonModel) -> None:
        """Добавить кнопку."""
        raise NotImplementedError

    @abstractmethod
    async def delete_message(self, delete_message_model: DeleteMessageModel) -> None:
        """Удалить сообщение."""
        raise NotImplementedError


    @abstractmethod
    async def delete_button(self, delete_button_model: DeleteButtonModel) -> None:
        """Удалить кнопку."""
        raise NotImplementedError
