from datetime import datetime, time

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Time, false, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.entities import Entity


class User(Entity):
    __tablename__ = "users"

    telegram_id: Mapped[BigInteger | None] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(String(32))
    first_name: Mapped[str | None] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    # phone_number: Mapped[str | None] = mapped_column(String(25))
    is_admin: Mapped[bool | None] = mapped_column(Boolean, server_default=false())
    is_moderator: Mapped[bool | None] = mapped_column(Boolean, server_default=false())
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    tab_namber: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    @property
    def url(self) -> str:
        return f"tg://user?id={self.telegram_id}"
