from pydantic import BaseModel

from ...AttributeService.schemas.types import AttributeTypeId
from .NodeId import NodeId


class NodeTreeSchema(BaseModel):
    id: NodeId
    type_id: AttributeTypeId
    attrs: dict[str, str]
    holder: bool
    children: list["NodeTreeSchema"]
