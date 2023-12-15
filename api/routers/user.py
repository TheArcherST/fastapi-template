from fastapi import APIRouter

from infrastructure.dto import BaseDTO

from domain.models import User
from api.dependencies.repos import AllUsersDep


router = APIRouter()


class CreateUserDTO(BaseDTO):
    first_name: str


class UserDTO(BaseDTO):
    id: int
    first_name: str

    @classmethod
    def from_model(cls, obj: User):
        return UserDTO(
            id=obj.id,
            first_name=obj.first_name,
        )


@router.post('/users/new')
async def create_new_user(
        payload: CreateUserDTO,
        all_users: AllUsersDep,
) -> UserDTO:
    new_user = User(
        first_name=payload.first_name,
    )
    await all_users.save(new_user)
    await all_users.commit()
    return UserDTO.from_model(new_user)


@router.post('/users/{user_id}')
async def get_user_by_id(
        user_id: int,
        all_users: AllUsersDep,
):
    result = await all_users.with_id(user_id)
    return UserDTO.from_model(result)
