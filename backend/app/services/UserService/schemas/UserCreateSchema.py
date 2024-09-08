from pydantic import BaseModel

from .UserId import UserId


class UserCreateSchema(BaseModel):
    id: UserId
