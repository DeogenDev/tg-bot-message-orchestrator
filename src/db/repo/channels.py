"""Таблица с каналами."""


from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.db.model_base import Base


class Channel(Base):
    __tablename__ = "channels"

    channel_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False
    )

    author_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    channel_username: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    author_username: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
