"""Инициализация репозиториев."""

from src.db.repo import ChannelRepo, MessageRepo

channel_repo = ChannelRepo()
message_repo = MessageRepo()
