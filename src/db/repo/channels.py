"""Репозиторий каналов."""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces.channels import ChannelRepoBase
from src.core.schemas.channel import ChannelModel, DeleteChannelModel

from src.db.models import Channel


class ChannelRepo(ChannelRepoBase):
    """Репозиторий каналов."""

    async def add_channel(
        self,
        session: AsyncSession,
        channel: ChannelModel
    ) -> None:
        """Добавить канал."""
        data = channel.model_dump(exclude_none=True)

        channel_db = Channel(**data)
        session.add(channel_db)
        await session.flush()

    async def get_channels(
        self,
        session: AsyncSession
    ) -> list[ChannelModel]:
        """Получить список каналов."""
        stmt = select(Channel)
        result = await session.execute(stmt)
        channels_db = result.scalars().all()

        return [
            ChannelModel.model_validate(channel, from_attributes=True)
            for channel in channels_db
        ]

    async def delete_channel(
        self,
        session: AsyncSession,
        delete_channel_model: DeleteChannelModel
    ) -> None:
        """Удалить канал."""
        stmt = delete(Channel).where(
            Channel.channel_id == delete_channel_model.channel_id
        )

        await session.execute(stmt)
        await session.flush()
