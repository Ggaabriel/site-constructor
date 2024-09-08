from app.registry import IRegistry

from ..AttributeService.schemas.NodeAttributeExternalSchema import (
    NodeAttributeExternalSchema,
)
from ..exceptions import TemplateDoesNotExistError
from ..NodeService.INodeService import INodeService
from ..NodeService.schemas.NodeId import NodeId
from ..NodeService.schemas.NodeTreeSchema import NodeTreeSchema
from .ITemplateService import ITemplateService
from .schemas.TemplateId import TemplateId
from .schemas.TemplateSchema import TemplateSchema
from .schemas.TemplateView import TemplateView


class TemplateService(ITemplateService):
    """
    A service class for managing node templates related operations
    """

    __node_service: INodeService
    __registry: IRegistry

    def __init__(self, registry: IRegistry) -> None:
        """
        Initialize the TemplateService with registry
        """
        self.__registry = registry

    async def inject_dependencies(self, node_service: INodeService) -> None:
        """
        Inject dependencies and prepopulate
        """
        self.__node_service = node_service
        await self.__prepopulate()

    async def get_all(self) -> list[TemplateId]:
        """
        Retrieve all templates

        Returns:
            list[TemplateId]: list of template ID
        """
        return [TemplateSchema(**template).id for template in self.__registry.read({})]

    async def get(self, template_id: TemplateId) -> TemplateView:
        """
        Receive a detailed information about template

        Args:
            template_id (TemplateId): template ID

        Raises:
            TemplateDoesNotExistError: raised when template with given ID does not exist

        Returns:
            TemplateView: An object representation of a template
        """
        result = self.__registry.get(template_id)
        if result is None:
            raise TemplateDoesNotExistError()
        template = TemplateSchema(**result)
        tree = await self.__node_service.get_tree(template.root_node_id)
        return TemplateView(id=template.id, tree=tree)

    async def create(self, node_id: NodeId) -> TemplateId:
        """
        Create a template from node

        Args:
            node_id (NodeId): ID of a node to be turned into a template

        Returns:
            TemplateId: ID of a created template
        """
        tree = await self.__node_service.get_tree(node_id)
        copied_tree = await self.__deep_copy(tree)
        template = TemplateSchema(root_node_id=copied_tree.id)
        self.__registry.create(template.id, template.model_dump(exclude={"id"}))
        return template.id

    async def delete(self, template_id: TemplateId) -> None:
        template = await self.get(template_id)
        await self.__node_service.delete(template.tree.id)
        self.__registry.delete(template_id)

    async def instantiate(self, template_id: TemplateId) -> NodeTreeSchema:
        """
        Instantiate a template

        Args:
            template_id (TemplateId): ID of a template to be instantiated

        Returns:
            NodeTreeSchema: instantiated (copied) template
        """
        root_node_id = await self.__get_root_node_id(template_id)
        tree = await self.__node_service.get_tree(root_node_id)
        copied_tree = await self.__deep_copy(tree)
        return copied_tree

    async def __deep_copy(self, tree: NodeTreeSchema) -> NodeTreeSchema:
        """
        Copy template and his progeny as a regular nodes

        Args:
            tree (NodeTreeSchema): Original template and his progeny

        Returns:
            NodeTreeSchema: copied NodeTree
        """
        copied_tree = tree.model_copy(deep=True)
        root_id = await self.__node_service.create(
            parent_id=None,
            node_attributes=NodeAttributeExternalSchema(
                type_id=copied_tree.type_id,
                attrs=copied_tree.attrs,
            ),
        )
        copied_tree.id = root_id
        stack = [(root_id, child) for child in copied_tree.children]
        while len(stack) > 0:
            parent_id, current = stack.pop()
            current.id = await self.__node_service.create(
                parent_id,
                NodeAttributeExternalSchema(
                    type_id=current.type_id, attrs=current.attrs
                ),
            )
            stack.extend([(current.id, child) for child in current.children])
        return copied_tree

    async def __get_root_node_id(self, templte_id: TemplateId) -> NodeId:
        """
        Get template's root node id

        Args:
            templte_id (TemplateId): ID of a template

        Raises:
            TemplateDoesNotExistError: raised when template with given id does not exist

        Returns:
            NodeId: ID of a root node
        """
        result = self.__registry.get(templte_id)
        if result is None:
            raise TemplateDoesNotExistError()
        template = TemplateSchema(**result)
        return template.root_node_id

    async def __prepopulate(self) -> None:
        """
        Prepopulate node and template registries with records
        """
        if not await self.get_all():
            container_id = await self.__node_service.create(
                parent_id=None,
                node_attributes=NodeAttributeExternalSchema(
                    type_id="container",
                    attrs={
                        "direction": "flex-col",
                        "background": "#ffffff",
                        "background_image": "false",
                    },
                ),
            )
            text_id = await self.__node_service.create(
                parent_id=None,
                node_attributes=NodeAttributeExternalSchema(
                    type_id="text",
                    attrs={
                        "position": "text-left",
                        "color": "#000000",
                        "text": "Text goes here",
                    },
                ),
            )
            image_id = await self.__node_service.create(
                parent_id=None,
                node_attributes=NodeAttributeExternalSchema(
                    type_id="image",
                    attrs={"rounded": ""},
                ),
            )
            await self.create(container_id)
            await self.create(text_id)
            await self.create(image_id)
