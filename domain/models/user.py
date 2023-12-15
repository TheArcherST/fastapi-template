from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.relational_entity import BaseRelationalEntity


class User(BaseRelationalEntity):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column()
