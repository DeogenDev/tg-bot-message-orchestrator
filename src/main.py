"""Файл запуска бота."""

import asyncio
import logging

from src.core.tg_bot import bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot")
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
