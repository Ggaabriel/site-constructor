from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.services import NodeService
from app.services.exceptions import (
    EndNodeError,
    NodeCannotBeDeletedError,
    NodeInDifferentTreeError,
    NodeNotFoundError,
    NotAllowedError,
    TemplateDoesNotExistError,
    UserNotFoundError,
)
from app.services.NodeService.schemas.NodeCreateSchema import NodeCreateSchema
from app.services.NodeService.schemas.NodeExtendedSchema import NodeExtendedSchema
from app.services.NodeService.schemas.NodeId import NodeId
from app.services.NodeService.schemas.NodeTreeSchema import NodeTreeSchema
from app.services.NodeService.schemas.NodeUpdateSchema import NodeUpdateSchema
from app.services.UserService.schemas.UserId import UserId

from .dependencies import get_node_service, get_user_id_by_init_data
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/nodes", tags=["Nodes"])


@router.get(
    "/{node_id}",
    response_model=NodeExtendedSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def node_get(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_id: NodeId,
) -> NodeExtendedSchema:
    try:
        return await node_service.try_get(initiator_id, node_id)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant see this node")


@router.get(
    "/tree/{node_id}",
    response_model=NodeTreeSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def node_get_tree(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_id: NodeId,
) -> NodeTreeSchema:
    try:
        return await node_service.try_get_tree(initiator_id, node_id)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant get this tree")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def node_add(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_create: NodeCreateSchema,
) -> str:
    try:
        return await node_service.try_create(initiator_id, node_create)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )
    except TemplateDoesNotExistError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A template with this ID does not exist"
        )
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant create this node")
    except EndNodeError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "You can't add a child to this node"
        )


@router.patch(
    path="/{node_id}",
    status_code=status.HTTP_200_OK,
    response_model=None,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def update_node(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_update: NodeUpdateSchema,
    node_id: NodeId,
) -> None:
    try:
        await node_service.try_update(initiator_id, node_id, node_update)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant update this node")
    except NodeInDifferentTreeError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Nodes can be reparented only in same tree"
        )


@router.delete(
    path="/{node_id}",
    status_code=status.HTTP_200_OK,
    response_model=None,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def delete_node(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_id: NodeId,
) -> None:
    try:
        await node_service.try_delete(initiator_id, node_id)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "The user with this ID was not found",
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant delete this node")
    except NodeCannotBeDeletedError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Can't delete root node")
