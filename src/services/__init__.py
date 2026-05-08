"""Сервисы приложения."""

from .channels import ChannelsService
from .messages import MessagesService

__all__ = [
    "ChannelsService",
    "MessagesService"
]
