"""Хендлеры бота."""

from .buttons import router as buttons_router
from .channels import router as channels_router
from .common import router as common_router
from .messages import router as messages_router

__all__ = [
    "buttons_router",
    "channels_router",
    "common_router",
    "messages_router"
]
