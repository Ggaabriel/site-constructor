from abc import ABC, abstractmethod

from ..NodeService.schemas.NodeId import NodeId
from .schemas.AttributeTypeSchema import AttributeTypeSchema
from .schemas.NodeAttributeExternalSchema import NodeAttributeExternalSchema
from .schemas.types import AttributeTypeId


class IAttributeService(ABC):
    @abstractmethod
    async def get_type(self, attribute_type: AttributeTypeId) -> AttributeTypeSchema:
        pass

    @abstractmethod
    async def get_all_types(self) -> list[AttributeTypeSchema]:
        pass

    @abstractmethod
    async def get_attribute(self, attribute_id: NodeId) -> NodeAttributeExternalSchema:
        pass

    @abstractmethod
    async def create_type(self, new_type: AttributeTypeSchema) -> None:
        pass

    @abstractmethod
    async def create_attribute(
        self, id: NodeId, new_node_attribute: NodeAttributeExternalSchema
    ) -> None:
        pass

    @abstractmethod
    async def delete_type(self, attribute_type: AttributeTypeId) -> None:
        pass

    @abstractmethod
    async def delete_attribute(self, attribute_id: NodeId) -> None:
        pass

    @abstractmethod
    async def update_node_attributes(
        self, node_id: NodeId, key: str, value: str
    ) -> None:
        pass

    @abstractmethod
    async def is_file_type(self, node_id: NodeId) -> bool:
        pass

    @abstractmethod
    async def exist_type(self, attribute_type: AttributeTypeId) -> bool:
        pass
