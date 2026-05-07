"""Модель данных канала."""

from pydantic import BaseModel, Field


class Channel(BaseModel):
    """Модель данных канала."""

    channel_id: int = Field(
        description="ID канала",
    )
    author_id: int = Field(
        ge=1,
        description="ID автора добавившего канал",
    )
    channel_username: str | None = Field(
        default=None,
        min_length=4,
        max_length=32,
        description="Никнейм канала",
    )
    title: str | None = Field(
        default=None,
        min_length=4,
        max_length=256,
        description="Название канала",
    )
    author_username: str | None = Field(
        default=None,
        min_length=4,
        max_length=32,
        description="Никнейм автора канала",
    )

class DeleteChannel(BaseModel):
    """Модель данных канала."""

    channel_id: int = Field(
        description="ID канала",
    )
