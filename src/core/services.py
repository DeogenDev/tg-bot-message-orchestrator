"""Инициализация сервисов."""

from src.services import ChannelsService, MessagesService
from .repo import channel_repo, message_repo


channels_service = ChannelsService(channel_repo)
messages_service = MessagesService(message_repo)
