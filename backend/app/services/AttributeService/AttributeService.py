import re

from app.registry import IRegistry

from ..exceptions import (
    AttributeDoesNotExistError,
    AttributeTypeAlreadyExists,
    AttributeTypeNotFoundError,
    InvalidAttributeValueError,
    NodeAttributeNotFoundError,
)
from ..FileService import IFileService
from ..NodeService.schemas.NodeId import NodeId
from .IAttributeService import IAttributeService
from .schemas.AttributeTypeSchema import AttributeTypeSchema
from .schemas.NodeAttributeExternalSchema import NodeAttributeExternalSchema
from .schemas.types import AttributeTypeId


class AttributeService(IAttributeService):
    """
    a service class for managing attributes-related operations
    """

    __type_registry: IRegistry
    __attribute_registry: IRegistry
    __file_service: IFileService
    __file_based_attribute_types = ["image", "container"]

    def __init__(self, type_registry: IRegistry, attribute_service: IRegistry) -> None:
        """
        initialize the AttributeService with two registries

        Args:
            type_registry (IRegistry): registry used for types of attributes
            attribute_service (IRegistry): registry used for attributes
        """
        self.__type_registry = type_registry
        self.__attribute_registry = attribute_service

    async def inject_dependencies(self, file_service: IFileService) -> None:
        """
        injects dependencies and prepopulates table
        """
        self.__file_service = file_service
        await self.__prepopulate_type()

    async def get_type(self, attribute_type: AttributeTypeId) -> AttributeTypeSchema:
        """
        returns information about type of attributes

        Args:
            attribute_type (AttributeTypeId): id of a type of attributes

        Raises:
            AttributeTypeNotFoundError: raised when type with given id does not exist

        Returns:
            AttributeTypeSchema: Pydantic schema representation of attribute type
        """
        result = self.__type_registry.get(attribute_type)
        if result is None:
            raise AttributeTypeNotFoundError()
        return AttributeTypeSchema(**result)

    async def get_all_types(self) -> list[AttributeTypeSchema]:
        """
        returns all attributes types

        Returns:
            list[AttributeTypeSchema]: list of pydantic schema representations of \
            attribute types
        """
        return [
            AttributeTypeSchema(**attribute_type)
            for attribute_type in self.__type_registry.read({})
        ]

    async def get_attribute(self, attribute_id: NodeId) -> NodeAttributeExternalSchema:
        """
        returns node-attribute

        Raises:
            NodeAttributeNotFoundError: raised when node-attribute with given id does \
            not exist

        Returns:
            NodeAttributeExternalSchema: Pydantic schema representation of a \
            node-attribute
        """

        result = self.__attribute_registry.get(attribute_id)
        if result is None:
            raise NodeAttributeNotFoundError()
        return NodeAttributeExternalSchema(**result)

    async def create_type(self, new_type: AttributeTypeSchema) -> None:
        """
        creates new attribute type

        Args:
            new_type (AttributeTypeSchema): data required to create new attribute type

        Raises:
            AttributeTypeAlreadyExists: raised when attribute type with given name \
            already exists
            InvalidAttributeValueError: raised when provided with invalid regex
        """
        if await self.exist_type(new_type.id):
            raise AttributeTypeAlreadyExists()
        for regex in new_type.attrs.values():
            try:
                re.compile(regex)
            except re.error:
                raise InvalidAttributeValueError()
        self.__type_registry.create(new_type.id, new_type.model_dump(exclude={"id"}))

    async def create_attribute(
        self, id: NodeId, new_node_attribute: NodeAttributeExternalSchema
    ) -> None:
        """
        create new node_attribute

        Args:
            id (NodeId): id of a node whoose attribute is to be created
            new_node_attribute (NodeAttributeExternalSchema): data required to create \
            new node-attribute

        Raises:
            AttributeTypeNotFoundError: raised when attribute type a new \
            node-attribute is invalid

        """
        node_type = await self.get_type(new_node_attribute.type_id)
        for key, value in new_node_attribute.attrs.items():
            await self.__validate_attribute(key, value, node_type)
        self.__attribute_registry.create(id, new_node_attribute.model_dump())

    async def delete_attribute(self, attribute_id: NodeId) -> None:
        """
        deletes node-attribute

        Args:
            attribute_id (NodeId): id of a node-attribute

        Raises:
            NodeAttributeNotFoundError: raised when node-attribute with given id does \
            not exist
        """
        if await self.is_file_type(attribute_id) and await self.__file_service.exists(
            attribute_id
        ):
            await self.__file_service.remove_file(attribute_id)
        self.__attribute_registry.delete(attribute_id)

    async def delete_type(self, attribute_id: AttributeTypeId) -> None:
        """
        delets attribute type

        Args:
            attribute_id (AttributeTypeId): id of an attribute type

        Raises:
            AttributeTypeNotFoundError: raised when attribute type with given id does \
            not exit
        """
        if not self.__type_registry.delete(attribute_id):
            raise AttributeTypeNotFoundError()

    async def update_node_attributes(
        self, node_id: NodeId, key: str, value: str
    ) -> None:
        """
        changes node-attribute value

        Args:
            node_id (NodeId): id of a node whose attribute you need to change
            key (str): what attribute to change
            value (str): new value for attribute

        Raises:
            InvalidAttributeValueError: raised when new value for attribute failes \
            validation
            AttributeDoesNotExistError: raised when given attribute does not exist in \
            node-attribute's list of attributes
        """

        node_attribute = await self.get_attribute(node_id)
        node_type = await self.get_type(node_attribute.type_id)
        await self.__validate_attribute(key, value, node_type)
        node_attribute.attrs.update({key: value})
        self.__attribute_registry.update(node_id, {"attrs": node_attribute.attrs})

    async def exist_type(self, attribute_id: AttributeTypeId) -> bool:
        """
        check if given attribute type exists

        Args:
            attribute_id (AttributeTypeId): id of an attribute type

        Returns:
            bool: returns true if exists and false when doesn't
        """
        attr_type = self.__type_registry.get(attribute_id)
        return attr_type is not None

    async def is_file_type(self, node_id: NodeId) -> bool:
        """
        checks if given node has node attribute type that belongs to a file types \

        Args:
            type (AttributeTypeId): attribute type id

        Returns:
            bool: returns true if attribute type belongs to file types, \
            returns false if attribute type does not belongs to file types
        """

        attrs = await self.get_attribute(node_id)
        return attrs.type_id in self.__file_based_attribute_types

    async def __validate_attribute(
        self, key: str, value: str, node_type: AttributeTypeSchema
    ) -> None:
        """
        validates attribute

        Args:
            key (str): attribute name
            value (str): new attribute value
            node_type (AttributeTypeSchema): object representation \
                of an node attribute type.

        Raises:
            AttributeDoesNotExistError: raised when attribute type does not contain \
                given attribute name
            InvalidAttributeValueError: raised when attribute new value is invalid
        """
        regex = node_type.attrs.get(key)
        if regex is None:
            raise AttributeDoesNotExistError()
        valid = re.match(regex, value)
        if valid is None:
            raise InvalidAttributeValueError()

    async def __prepopulate_type(self) -> None:
        """
        prepolates type table with attribute types
        """
        if not await self.get_all_types():
            await self.create_type(
                AttributeTypeSchema(
                    id="container",
                    attrs={
                        "direction": "^flex-(row|col)$",
                        "background": "^#(?:[0-9a-fA-F]{3}){1,2}$",
                        "background_image": "^true|false$",
                    },
                )
            )
            await self.create_type(
                AttributeTypeSchema(
                    id="text",
                    attrs={
                        "position": "^text-(left|right|center)$",
                        "color": "^#(?:[0-9a-fA-F]{3}){1,2}$",
                        "text": "^.{1,50}$",
                    },
                )
            )
            await self.create_type(
                AttributeTypeSchema(
                    id="image",
                    attrs={
                        "rounded": "^(rounded){0,1}(-md|-lg|-full){0,1}$",
                    },
                )
            )
