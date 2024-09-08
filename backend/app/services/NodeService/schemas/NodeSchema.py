from uuid import uuid4

from pydantic import BaseModel, Field

from .NodeId import NodeId


class NodeSchema(BaseModel):
    parent: NodeId | None
    id: NodeId = Field(default_factory=lambda: NodeId(str(uuid4())))
    children: list[NodeId] = []
