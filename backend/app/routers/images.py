from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status

from app.services.exceptions import (
    FileDoesNotExistError,
    FileTooBigError,
    IncompatibleNodeError,
    InvalidFileFormatError,
    NodeAttributeNotFoundError,
    NotAllowedError,
)
from app.services.ImageService.ImageService import ImageService
from app.services.NodeService.schemas.NodeId import NodeId
from app.services.UserService.schemas.UserId import UserId

from .dependencies import get_image_service, get_user_id_by_init_data
from .exceptions import HTTPExceptionSchema
from .utils import FileWrapper

router = APIRouter(prefix="/images", tags=["Images"])


@router.post(
    "/",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
    },
)
async def add_image_to_node(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    image_service: Annotated[ImageService, Depends(get_image_service)],
    node_id: Annotated[NodeId, Form()],
    file: UploadFile,
) -> None:
    try:
        await image_service.add_image(node_id, FileWrapper(file))
    except InvalidFileFormatError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid file format")
    except NodeAttributeNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Node does not exist")
    except IncompatibleNodeError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Node does not support images")
    except FileTooBigError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File too big")


@router.delete(
    "/{node_id}/",
    response_model=None,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
    },
)
async def delete_image(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    image_service: Annotated[ImageService, Depends(get_image_service)],
    node_id: NodeId,
) -> None:
    try:
        await image_service.remove_image(node_id)
    except FileDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Node does not exist")
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You can't delete this image")
