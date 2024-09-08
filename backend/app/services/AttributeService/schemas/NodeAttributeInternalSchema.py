from ...NodeService.schemas.NodeId import NodeId
from .NodeAttributeExternalSchema import NodeAttributeExternalSchema


class NodeAttributeInternalSchema(NodeAttributeExternalSchema):
    id: NodeId
