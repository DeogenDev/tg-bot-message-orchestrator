"""Репозиторий сообщений."""

from sqlalchemy import delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces.messages import MessageRepoBase
from src.core.schemas.message import (
    MessageModel,
    DeleteMessageModel,
    DeleteButtonModel,
    ButtonModel,
)

from src.db.models import Message, Button


class MessageRepo(MessageRepoBase):
    """Репозиторий каналов."""

    async def add_message(
        self,
        session: AsyncSession, 
        message_model: MessageModel
    ) -> None:
        """Добавить канал."""
        data = message_model.model_dump(exclude_none=True) 

        message_db = Message(**data)
        session.add(message_db)
        await session.flush()

    async def edit_message(
        self,
        session: AsyncSession, 
        message_model: MessageModel
    ) -> None:
        """Обновить только текст сообщения."""
        data = message_model.model_dump(exclude_none=True, exclude={'buttons'})

        stmt = (
            update(Message)
            .where(Message.id == message_model.id)
            .values(**data)
        )

        await session.execute(stmt)
        await session.flush()

    async def get_messages(
            self,
            session: AsyncSession
    ):
        """Получить список сообщений."""
        stmt = select(Message)
        result = await session.execute(stmt)
        messages_db = result.scalars().all()

        return [
            MessageModel.model_validate(message, from_attributes=True)
            for message in messages_db
        ]

    async def add_button(
        self, 
        session: AsyncSession, 
        button_model: ButtonModel
    ) -> None:
        """Добавить кнопку."""
        data = button_model.model_dump(exclude_none=True) 

        button_db = Button(**data)
        session.add(button_db)
        await session.flush()

    async def delete_message(
        self, 
        session: AsyncSession,
        delete_message_model: DeleteMessageModel
    ) -> None:
        """Удалить сообщение."""
        stmt = delete(Message).where(Message.id == delete_message_model.id)

        await session.execute(stmt)
        await session.flush()

    async def delete_button(
        self,
        session: AsyncSession,
        delete_button_model: DeleteButtonModel
    ) -> None:
        """Удалить кнопку."""
        stmt = delete(Button).where(Button.id == delete_button_model.id)

        await session.execute(stmt)
        await session.flush()
