"""Модель данных сообщения."""

from pydantic import BaseModel, Field, field_validator

class ButtonModel(BaseModel):
    """Модель данных кнопки."""

    id: int = Field(
        ge=1,
        description="ID кнопки"
    )

    text: str = Field(
        min_length=1,
        max_length=64,
        description="Текст на кнопке (лучше до 20-30 символов, чтобы не обрезался)"
    )
    url: str = Field(
        max_length=256,
        description="URL кнопки (лимит TG — 256 байт)"
    )
    column: int = Field(
        ge=1,
        le=8,
        description="Номер колонки (в ряду макс 8 кнопок)"
    )
    row: int = Field(
        ge=1,
        le=100,
        description="Номер ряда (всего макс 100 кнопок)"
    )

    message_id: int = Field(
        description="ID сообщения",
    )

    @field_validator("url")
    @classmethod
    def validate_url_scheme(cls, v: str) -> str:
        if not v.startswith(("http://", "https://", "tg://")):
            raise ValueError("URL должен начинаться с http, https или tg")
        return v

class DeleteButtonModel(BaseModel):
    """Модель данных кнопки."""

    id: int = Field(
        ge=1, 
        description="ID кнопки"
    )

class MessageModel(BaseModel):
    """Модель данных сообщения."""

    id: int | None = Field(
        ge=1,
        description="ID сообщения"
    )
    text: str = Field(
        min_length=1,
        max_length=4096,
        description="Текст сообщения (лимит TG — 4096 байт)"
    )
    buttons: list[ButtonModel] | None = Field(
        max_items=100,
        description="Кнопки (лимит TG — 100 кнопок)"
    )

class DeleteMessageModel(BaseModel):
    """Модель данных сообщения."""

    id: int = Field(
        ge=1,
        description="ID сообщения"
    )
