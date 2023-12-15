from typing import TypeAlias, Annotated

from domain import repos
from fastapi import Depends

from .session import DatabaseSessionDep


async def get_all_users(session: DatabaseSessionDep):
    return repos.AllUsers(session)


AllUsersDep: TypeAlias = Annotated[repos.AllUsers, Depends(get_all_users)]
