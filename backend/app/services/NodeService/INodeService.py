from abc import ABC, abstractmethod

from ..AttributeService.schemas.NodeAttributeExternalSchema import (
    NodeAttributeExternalSchema,
)
from ..UserService.schemas.UserId import UserId
from .schemas.NodeCreateSchema import NodeCreateSchema
from .schemas.NodeExtendedSchema import NodeExtendedSchema
from .schemas.NodeId import NodeId
from .schemas.NodeTreeSchema import NodeTreeSchema
from .schemas.NodeUpdateSchema import NodeUpdateSchema


class INodeService(ABC):
    @abstractmethod
    async def try_get(
        self, initiator_id: UserId, node_id: NodeId
    ) -> NodeExtendedSchema:
        pass

    @abstractmethod
    async def try_update(
        self, initiator_id: UserId, node_id: NodeId, node_update: NodeUpdateSchema
    ) -> None:
        pass

    @abstractmethod
    async def try_get_tree(
        self, initiator_id: UserId, node_id: NodeId
    ) -> NodeTreeSchema:
        pass

    @abstractmethod
    async def try_delete(self, initiator_id: UserId, node_id: NodeId) -> None:
        pass

    @abstractmethod
    async def try_create(
        self, initiator_id: UserId, new_node: NodeCreateSchema
    ) -> NodeId:
        pass

    @abstractmethod
    async def create(
        self, parent_id: NodeId | None, node_attributes: NodeAttributeExternalSchema
    ) -> NodeId:
        pass

    @abstractmethod
    async def exist(self, node_id: NodeId) -> bool:
        pass

    @abstractmethod
    async def get_tree(self, node_id: NodeId) -> NodeTreeSchema:
        pass

    @abstractmethod
    async def delete(self, node_id: NodeId) -> None:
        pass
