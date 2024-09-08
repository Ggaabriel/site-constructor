from pydantic import BaseModel

from ...TemplateService.schemas.TemplateId import TemplateId
from .NodeId import NodeId


class NodeCreateSchema(BaseModel):
    parent: NodeId
    template_id: TemplateId
