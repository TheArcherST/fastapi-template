from typing import TypeAlias

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncSession, AsyncAttrs, create_async_engine
)

from config import config


async_engine = create_async_engine('postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'.format(
    user=config.postgres_user,
    password=config.postgres_password,
    host=config.postgres_host,
    port=config.postgres_port,
    dbname=config.postgres_db,
))


class RelationalMapper(DeclarativeBase, AsyncAttrs):
    pass


DatabaseSession: TypeAlias = AsyncSession


def get_database_session() -> DatabaseSession:
    return AsyncSession(async_engine, expire_on_commit=False)


async def on_startup():
    from domain import models  # noqa
    async with async_engine.connect() as conn:
        await conn.run_sync(RelationalMapper.metadata.create_all)
        await conn.commit()


__all__ = [
    "RelationalMapper",
    "DatabaseSession",
    "get_database_session",
    "on_startup",
]
