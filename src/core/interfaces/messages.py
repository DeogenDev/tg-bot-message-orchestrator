"""Интерфейс сообщений."""

from abc import ABC, abstractmethod

from src.core.schemas.message import MessageModel, DeleteMessage, DeleteButton, Button


class MessageRepoBase(ABC):
    """Интерфейс для управления сообщениями."""

    @abstractmethod
    def add_message(self, message: MessageModel) -> None:
        """Добавить сообщение."""
        raise NotImplementedError

    @abstractmethod
    def get_messages(self) -> list[MessageModel]:
        """Получить список сообщений."""
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, delete_message_model: DeleteMessage) -> None:
        """Удалить сообщение."""
        raise NotImplementedError

    @abstractmethod
    def add_button(self, button: Button) -> None:
        """Добавить кнопку."""
        raise NotImplementedError

    @abstractmethod
    def delete_button(self, delete_button_model: DeleteButton) -> None:
        """Удалить кнопку."""
        raise NotImplementedError
