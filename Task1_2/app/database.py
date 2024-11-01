import os
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


DATABASE_URL = f"sqlite+aiosqlite:///{os.path.abspath('database.db')}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class URLS(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    original_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    short_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    extend_existing = True
