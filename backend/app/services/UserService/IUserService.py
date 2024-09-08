from abc import ABC, abstractmethod

from .schemas.UserCreateSchema import UserCreateSchema
from .schemas.UserId import UserId
from .schemas.UserSchema import UserSchema


class IUserService(ABC):
    @abstractmethod
    async def try_get_by_id(self, initiator_id: UserId, user_id: UserId) -> UserSchema:
        pass

    @abstractmethod
    async def create(self, new_user: UserCreateSchema) -> None:
        pass

    @abstractmethod
    async def user_exist_validation(self, user_id: UserId) -> None:
        pass

    @abstractmethod
    async def exist(self, user_id: UserId) -> bool:
        pass
