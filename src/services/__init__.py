"""Сервисы приложения."""

from .channels import ChannelService
from .messages import MessagesService

__all__ = [
    "ChannelService",
    "MessagesService"
]
