"""Таблица с сообщениями."""

from typing import  List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.model_base import Base


if TYPE_CHECKING:
    from .buttons import Button


class Message(Base):
    """Таблица с сообщениями."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    buttons: Mapped[List["Button"]] = relationship(
        back_populates="message", 
        cascade="all, delete-orphan"
    )
