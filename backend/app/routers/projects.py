from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.services import ProjectService
from app.services.exceptions import (
    NotAllowedError,
    ProjectNotFoundError,
    UserNotFoundError,
    WrongInitiatorError,
)
from app.services.ProjectService.schemas.ProjectCreateSchema import ProjectCreateSchema
from app.services.ProjectService.schemas.ProjectId import ProjectId
from app.services.ProjectService.schemas.ProjectSchema import ProjectSchema
from app.services.ProjectService.schemas.ProjectUpdateSchema import ProjectUpdateSchema
from app.services.UserService.schemas.UserId import UserId

from .dependencies import get_project_service, get_user_id_by_init_data
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/{project_id}",
    response_model=ProjectSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def project_get(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    project_id: ProjectId,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectSchema:
    try:
        return await project_service.try_get(initiator_id, project_id)
    except WrongInitiatorError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong initiator")
    except ProjectNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A project with this ID does not exist"
        )
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You do not have permission to view this project"
        )


@router.get(
    "/by/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ProjectSchema],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def project_get_user(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    user_id: UserId,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> list[ProjectSchema]:
    try:
        return await project_service.try_get_by_user_id(initiator_id, user_id)
    except WrongInitiatorError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong initiator")
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "You do not have permission to view this user's projects",
        )


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def project_add(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    project_create: ProjectCreateSchema,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectSchema:
    try:
        return await project_service.create(initiator_id, project_create)
    except WrongInitiatorError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong initiator")
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "The user with this ID was not found"
        )


@router.patch(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def update_project(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    project_update: ProjectUpdateSchema,
    project_id: ProjectId,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    try:
        await project_service.try_update(initiator_id, project_id, project_update)
    except WrongInitiatorError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong initiator")
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "You do not have permission to update this project",
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A project with this ID does not exist"
        )


@router.delete(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def project_delete(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    project_id: ProjectId,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    try:
        await project_service.try_delete(initiator_id, project_id)
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "You do not have permission to delete this project",
        )
    except WrongInitiatorError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "The user with this ID was not found",
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A project with this ID does not exist"
        )
