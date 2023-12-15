from typing import TYPE_CHECKING

from infrastructure.entity import BaseEntity
from infrastructure.database import RelationalMapper


class BaseRelationalObject(BaseEntity, RelationalMapper):
    __abstract__ = True


class BaseRelationalEntity(BaseRelationalObject):
    __abstract__ = True

    if TYPE_CHECKING:  # I believe in the developers' neatness
        id: int


__all__ = [
    "BaseRelationalObject",
    "BaseRelationalEntity",
]
