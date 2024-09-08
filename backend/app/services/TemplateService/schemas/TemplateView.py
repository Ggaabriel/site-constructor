from pydantic import BaseModel

from ...NodeService.schemas.NodeTreeSchema import NodeTreeSchema
from .TemplateId import TemplateId


class TemplateView(BaseModel):
    id: TemplateId
    tree: NodeTreeSchema
