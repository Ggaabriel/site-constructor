from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.services.exceptions import NotAllowedError, ProjectNotFoundError
from app.services.HTMLService import IHTMLService
from app.services.ProjectService.schemas.ProjectId import ProjectId
from app.services.UserService.schemas.UserId import UserId

from .dependencies import get_html_service, get_user_id_by_init_data
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/pages", tags=["Pages"])


@router.post(
    "/{project_id}/",
    response_model=None,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
    },
)
async def save_index_page(
    html_service: Annotated[IHTMLService, Depends(get_html_service)],
    project_id: ProjectId,
    initiator_id: Annotated[UserId, Depends(get_user_id_by_init_data)],
) -> None:
    try:
        await html_service.render_index_page(
            initiator_id=initiator_id, project_id=project_id
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Project with this id does not exist"
        )
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You can't save this project")
