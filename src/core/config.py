"""Настроки бота."""

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseModel):
    token: str = Field(
        description="Токен бота от @BotFather"
    )
    allowed_users: list[int] = Field(
        default_factory=list,
        description="Список Telegram ID с доступом"
    )

    @field_validator("token")
    @classmethod
    def validate_token(cls, v: str) -> str:
        if ":" not in v:
            raise ValueError("Некорректный формат токена. Проверьте ':'")
        return v

    @field_validator("allowed_users", mode="after")
    @classmethod
    def unique_users(cls, v: list[int]) -> list[int]:
        return list(set(v))


class DBConfig(BaseModel):
    host: str = Field(
        default="localhost",
        description="Адрес хоста"
    )
    port: int = Field(
        default=5432,
        description="Порт"
    )
    user: str = Field(
        description="Пользователь"
    )
    password: str = Field(
        description="Пароль"
    )
    database: str = Field(
        description="База данных"
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if v < 1 or v > 65535:
            raise ValueError("Некорректный порт")
        return v

    @property
    def dsn(self) -> str:
        """Собирает URL для асинхронного движка."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class Config(BaseSettings):
    bot: BotConfig
    database: DBConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


conf = Config()
