from pydantic import BaseModel

from .NodeId import NodeId


class NodeUpdateSchema(BaseModel):
    parent: NodeId
    position: int
