from abc import ABC, abstractmethod

from ..ProjectService.schemas.ProjectId import ProjectId
from ..UserService.schemas.UserId import UserId


class IHTMLService(ABC):
    @abstractmethod
    async def render_index_page(
        self, initiator_id: UserId, project_id: ProjectId
    ) -> None:
        pass
