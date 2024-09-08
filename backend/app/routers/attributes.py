from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.services.AttributeService.AttributeService import AttributeService
from app.services.exceptions import (
    AttributeDoesNotExistError,
    InvalidAttributeValueError,
    NodeAttributeNotFoundError,
)
from app.services.NodeService.schemas.NodeId import NodeId
from app.services.UserService.schemas.UserId import UserId

from .dependencies import get_attributes_service, get_user_id_by_init_data
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/attrs", tags=["Attributes"])


@router.patch(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
    },
)
async def node_attribute_update(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    attribute_service: Annotated[AttributeService, Depends(get_attributes_service)],
    node_id: NodeId,
    attribute_name: str,
    attribute_value: str,
) -> None:
    try:
        await attribute_service.update_node_attributes(
            node_id, attribute_name, attribute_value
        )
    except InvalidAttributeValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid attribute value")
    except AttributeDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Attribute does not exist")
    except NodeAttributeNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "NodeAttribute does not exist")
