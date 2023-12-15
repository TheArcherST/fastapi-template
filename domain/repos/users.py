from infrastructure.repo import BaseEntityRepo

from domain.models import User


class AllUsers(BaseEntityRepo[User]):
    pass
