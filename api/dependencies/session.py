from typing import Annotated, TypeAlias

from fastapi import Depends

from infrastructure.database import get_database_session as _get_database_session, DatabaseSession


async def get_database_session() -> DatabaseSession:
    async with _get_database_session() as session:
        yield session


DatabaseSessionDep: TypeAlias = Annotated[DatabaseSession, Depends(get_database_session)]
