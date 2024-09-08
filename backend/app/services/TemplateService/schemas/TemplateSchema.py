import uuid

from pydantic import BaseModel, Field

from ...NodeService.schemas.NodeId import NodeId
from .TemplateId import TemplateId


class TemplateSchema(BaseModel):
    id: TemplateId = Field(default_factory=lambda: TemplateId(str(uuid.uuid4())))
    root_node_id: NodeId
