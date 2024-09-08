from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.services.exceptions import NodeNotFoundError, TemplateDoesNotExistError
from app.services.NodeService.schemas.NodeId import NodeId
from app.services.TemplateService.schemas.TemplateId import TemplateId
from app.services.TemplateService.schemas.TemplateView import TemplateView
from app.services.TemplateService.TemplateService import TemplateService
from app.services.UserService.schemas.UserId import UserId

from .dependencies import get_template_service, get_user_id_by_init_data
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/templates", tags=["Templates"])


@router.get(
    path="/",
    response_model=list[TemplateId],
)
async def get_all_templates(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    template_service: Annotated[TemplateService, Depends(get_template_service)],
) -> list[TemplateId]:
    return await template_service.get_all()


@router.get(
    path="/{template_id}",
    response_model=TemplateView,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def get_template(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    template_id: Annotated[TemplateId, Path()],
    template_service: Annotated[TemplateService, Depends(get_template_service)],
) -> TemplateView:
    try:
        return await template_service.get(template_id)
    except TemplateDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Template does not exist")


@router.post(
    path="/",
    response_model=TemplateId,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
async def create_template(
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
    node_id: NodeId,
    template_service: Annotated[TemplateService, Depends(get_template_service)],
) -> TemplateId:
    try:
        return await template_service.create(node_id)
    except NodeNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Node does not exist")
