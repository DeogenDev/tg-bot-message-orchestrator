"""Модель данных для кнопок."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.db.model_base import Base


if TYPE_CHECKING:
    from .messages import Message

class Button(Base):
    """Модель данных для кнопок."""

    __tablename__ = "buttons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    column: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    row: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    message_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("messages.id")
    )
    message: Mapped["Message"] = relationship(
        back_populates="buttons"
    )
