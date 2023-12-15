from typing import (
    Generic, TypeVar, Optional, Iterable, ClassVar, get_origin, get_args,
    AsyncIterable, Any,
)

from sqlalchemy import select, func

from infrastructure.relational_entity import (
    BaseRelationalObject,
    BaseRelationalEntity,
)
from infrastructure.database import DatabaseSession


RelationalObjectT = TypeVar("RelationalObjectT", bound=BaseRelationalObject)
RelationalEntityT = TypeVar("RelationalEntityT", bound=BaseRelationalEntity)


class BaseRepo(Generic[RelationalObjectT]):
    _cls_model: ClassVar[Any] = None

    def __init__(
            self,
            session: DatabaseSession,
    ):
        self.session = session
        self._model: Optional[RelationalObjectT] = self._cls_model

    def __init_subclass__(cls):
        for j in getattr(cls, "__orig_bases__", []):
            if not issubclass(get_origin(j), BaseRepo):
                continue

            generic_args = get_args(j)

            if not generic_args:
                raise RuntimeError(
                    "Repository implementation infuse you to set "
                    "generic argument with an entity model."
                )

            type_ = generic_args[0]

            if isinstance(type_, TypeVar):
                continue

            cls._cls_model = type_
            return

    async def commit(self) -> None:
        await self.session.commit()

    async def save(
            self,
            obj: RelationalObjectT
    ) -> None:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def refresh(
            self,
            obj: RelationalEntityT,
            attribute_names: Optional[Iterable[str]] = None,
    ) -> RelationalObjectT:
        await self.session.refresh(obj, attribute_names)
        return obj

    async def iter(self) -> AsyncIterable[RelationalObjectT]:
        stmt = select(self._model)
        return await self.session.stream_scalars(stmt)


class BaseEntityRepo(BaseRepo[RelationalEntityT]):
    async def with_id(self, id_: int) -> Optional[RelationalEntityT]:
        # noinspection PyTypeChecker
        stmt = (select(self._model)
                .where(self._model.id == id_))
        return await self.session.scalar(stmt)

    async def count(self) -> int:
        stmt = select(func.count(self._model.id))
        return await self.session.scalar(stmt)


__all__ = [
    "BaseRepo",
    "BaseEntityRepo",
]
