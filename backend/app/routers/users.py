from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.services import UserService
from app.services.exceptions import (
    NotAllowedError,
    UserExistError,
    UserNotFoundError,
    WrongInitiatorError,
)
from app.services.UserService.schemas.UserCreateSchema import UserCreateSchema
from app.services.UserService.schemas.UserId import UserId
from app.services.UserService.schemas.UserSchema import UserSchema

from .dependencies import get_user_id_by_init_data, get_user_service
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def user_get(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    user_id: UserId,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserSchema:
    try:
        return await user_service.try_get_by_id(initiator_id, user_id)
    except WrongInitiatorError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "The user with this ID was not found"
        )
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You do not have permission to receive this user"
        )
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "The user with this ID was not found"
        )


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": HTTPExceptionSchema},
    },
)
async def user_add(
    user: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    try:
        await user_service.create(user)
    except UserExistError:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exist")
