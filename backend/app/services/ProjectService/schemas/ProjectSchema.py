from uuid import uuid4

from pydantic import Field

from ...NodeService.schemas.NodeId import NodeId
from ...UserService.schemas.UserId import UserId
from .ProjectCreateSchema import ProjectCreateSchema
from .ProjectId import ProjectId


class ProjectSchema(ProjectCreateSchema):
    id: ProjectId = Field(default_factory=lambda: ProjectId(str(uuid4())))
    core_node_id: NodeId
    owner_id: UserId
