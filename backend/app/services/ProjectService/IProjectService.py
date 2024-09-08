from abc import ABC, abstractmethod

from ..NodeService.schemas.NodeId import NodeId
from ..UserService.schemas.UserId import UserId
from .schemas.ProjectCreateSchema import ProjectCreateSchema
from .schemas.ProjectId import ProjectId
from .schemas.ProjectSchema import ProjectSchema
from .schemas.ProjectUpdateSchema import ProjectUpdateSchema


class IProjectService(ABC):
    @abstractmethod
    async def try_get_by_user_id(
        self, initiator_id: UserId, user_id: UserId
    ) -> list[ProjectSchema]:
        pass

    @abstractmethod
    async def try_get(
        self, initiator_id: UserId, project_id: ProjectId
    ) -> ProjectSchema:
        pass

    @abstractmethod
    async def get(self, project_id: ProjectId) -> ProjectSchema:
        pass

    @abstractmethod
    async def create(
        self, initiator_id: UserId, new_project: ProjectCreateSchema
    ) -> ProjectSchema:
        pass

    @abstractmethod
    async def try_update(
        self,
        initiator_id: UserId,
        project_id: ProjectId,
        project_update: ProjectUpdateSchema,
    ) -> None:
        pass

    @abstractmethod
    async def try_delete(self, initiator_id: UserId, project_id: ProjectId) -> None:
        pass

    @abstractmethod
    async def get_by_root_node_id(self, node_id: NodeId) -> ProjectSchema:
        pass
