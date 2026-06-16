"""Инициализация тг бота."""

from src.bot.bot import TelegramBot
from .services import channels_service, messages_service
from .config import conf


bot = TelegramBot(
    token=conf.bot.token,
    allowed_users=conf.bot.allowed_users,
    forward_group_id=conf.bot.forward_group_id,
    channels_service=channels_service,
    messages_service=messages_service
)
