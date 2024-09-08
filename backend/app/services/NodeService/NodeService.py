from app.registry import IRegistry

from ..AttributeService import IAttributeService
from ..AttributeService.schemas.NodeAttributeExternalSchema import (
    NodeAttributeExternalSchema,
)
from ..exceptions import (
    EndNodeError,
    IncompatibleNodeError,
    NodeCannotBeDeletedError,
    NodeInDifferentTreeError,
    NodeNotFoundError,
    NotAllowedError,
)
from ..ProjectService.IProjectService import IProjectService
from ..TemplateService.ITemplateService import ITemplateService
from ..UserService.IUserService import IUserService
from ..UserService.schemas.UserId import UserId
from .INodeService import INodeService
from .schemas.NodeCreateSchema import NodeCreateSchema
from .schemas.NodeExtendedSchema import NodeExtendedSchema
from .schemas.NodeId import NodeId
from .schemas.NodeSchema import NodeSchema
from .schemas.NodeTreeSchema import NodeTreeSchema
from .schemas.NodeUpdateSchema import NodeUpdateSchema


class NodeService(INodeService):
    """
    A service class for managing node-related operations.
    """

    __registry: IRegistry
    __user_service: IUserService
    __project_service: IProjectService
    __attribute_service: IAttributeService
    __template_service: ITemplateService

    def __init__(
        self,
        registry: IRegistry,
    ) -> None:
        """
        Initialize the NodeService with registry

        Args:
            registry (IRegistry): the registry used for node operations
        """
        self.__registry = registry

    async def inject_dependencies(
        self,
        user_service: IUserService,
        project_service: IProjectService,
        template_service: ITemplateService,
        attribute_service: IAttributeService,
    ) -> None:
        """
        injects dependencies

        Args:
            user_service (IUserService): service for interacting with users
            project_service (IProjectService): service for interacting with projects
            template_service (ITemplateService): service for interacting with templates
        """
        self.__user_service = user_service
        self.__project_service = project_service
        self.__template_service = template_service
        self.__attribute_service = attribute_service

    async def try_get(
        self, initiator_id: UserId, node_id: NodeId
    ) -> NodeExtendedSchema:
        """
        try get node

        Args:
            initiator_id (str): user id
            node_id (str): id of node

        Returns:
        NodeSchema: dict representation of node stored in database

        Raises:
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised when operation is performed by user who does not \
            own the project node belongs to
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """

        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, node_id)
        node_exp = await self.__get_extended(node_id)
        return node_exp

    async def try_update(
        self, initiator_id: UserId, node_id: NodeId, node_update: NodeUpdateSchema
    ) -> None:
        """
        update node

        Args:
            initiator_id (str): user id
            node_id (str): id of a node
            node_update (NodeUpdateSchema): dict representation of data \
                used to update node

        Raises:
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised when user tries to update node from project \
            they do not own
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
            NodeInDifferentTreeError: raised when trying reparent node to different tree
        """
        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, node_id)
        node = await self.__get(node_id)

        if not node.parent == node_update.parent:
            if not await self.__in_same_tree(node_id, node_update.parent):
                raise NodeInDifferentTreeError()
            await self.__reparent(node_id, node_update.parent)
        await self.__change_position(node_id, node_update.position)

    async def try_get_tree(
        self, initiator_id: UserId, node_id: NodeId
    ) -> NodeTreeSchema:
        """
        Try get subtree preresentation of a node and subnodes

        Args:
            initiator_id (str): user id
            node_id (str): node id

        Returns:
            NodeTreeSchema: tree representation of a node and subnodes

        Raises:
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised when user tries to update node from project \
                they do not own
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, node_id)

        node_tree = await self.get_tree(node_id)
        return node_tree

    async def try_delete(self, initiator_id: UserId, node_id: NodeId) -> None:
        """
        try delete

        Args:
            initiator_id (str): user id
            node_id (str): node id

        Raises:
            NodeCannotBeDeleted: raised when attempting to delete root node
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised when user tries to update node from project \
            they do not own
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, node_id)

        node = await self.__get(node_id)
        if node.parent is None:
            raise NodeCannotBeDeletedError()
        await self.delete(node_id)

    async def try_create(
        self, initiator_id: UserId, new_node: NodeCreateSchema
    ) -> NodeId:
        """
        create node

        Args:
            initiator_id (str): id of a user
            new_node (NodeCreateSchema): new node data

        Returns:
            str: id of a new node

        Raises:
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised if user tries to add a new node to a project they \
                do not own
            NodeNotFoundError: raised when there is no node with id provided \
                by new_node
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, new_node.parent)
        parent_attributes = await self.__attribute_service.get_attribute(
            new_node.parent
        )
        parent_type = await self.__attribute_service.get_type(parent_attributes.type_id)
        if not parent_type.holder:
            raise EndNodeError()
        instantiated_tree = await self.__template_service.instantiate(
            new_node.template_id
        )
        await self.__reparent(instantiated_tree.id, new_node.parent)
        # TODO: return NodeTreeSchema
        return instantiated_tree.id

    async def create(
        self, parent_id: NodeId | None, node_attributes: NodeAttributeExternalSchema
    ) -> NodeId:
        # TODO: docstring
        new_node = NodeSchema(parent=parent_id)
        self.__registry.create(new_node.id, new_node.model_dump(exclude={"id"}))
        await self.__attribute_service.create_attribute(new_node.id, node_attributes)

        if parent_id is not None:
            parent = await self.__get(parent_id)
            parent.children.append(new_node.id)
            self.__registry.update(parent.id, parent.model_dump(exclude={"id"}))
        return new_node.id

    async def exist(self, node_id: NodeId) -> bool:
        """
        check if node exist

        Args:
            node_id (str): id of a node to check

        Returns:
            bool: bool result depicting existence of a node
        """
        node = self.__registry.get(node_id)
        return node is not None

    async def get_tree(self, node_id: NodeId) -> NodeTreeSchema:
        """
        Get tree representation of node and subnodes

        Args:
            node_id (str): id of a node

        Returns:
            NodeTreeSchema: tree representaion of a node and subnodes

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        attributes = await self.__attribute_service.get_attribute(node_id)
        attribute_type = await self.__attribute_service.get_type(attributes.type_id)
        tree_root = NodeTreeSchema(
            id=node_id,
            type_id=attributes.type_id,
            attrs=attributes.attrs,
            holder=attribute_type.holder,
            children=[],
        )
        nodes_to_process = [tree_root]
        while len(nodes_to_process) > 0:
            current_tree_node = nodes_to_process.pop()
            current_node = await self.__get(current_tree_node.id)
            for child_node_id in current_node.children:
                child_attributes = await self.__attribute_service.get_attribute(
                    child_node_id
                )
                child_attribute_type = await self.__attribute_service.get_type(
                    child_attributes.type_id
                )
                current_tree_node.children.append(
                    NodeTreeSchema(
                        id=child_node_id,
                        type_id=child_attributes.type_id,
                        attrs=child_attributes.attrs,
                        holder=child_attribute_type.holder,
                        children=[],
                    )
                )
            nodes_to_process.extend(current_tree_node.children)
        return tree_root

    async def __get(self, node_id: NodeId) -> NodeSchema:
        """
        get node directly from database

        Args:
            node_id (str): node id

        Raises:
            NodeNotFoundError: raised when node with given id does not exist

        Returns:
            NodeSchema: dict representation of node
        """
        node = self.__registry.get(node_id)
        if node is None:
            raise NodeNotFoundError()
        return NodeSchema(**node)

    async def __get_extended(self, node_id: NodeId) -> NodeExtendedSchema:
        node = await self.__get(node_id)
        attributes = await self.__attribute_service.get_attribute(node.id)
        attribute_type = await self.__attribute_service.get_type(attributes.type_id)
        return NodeExtendedSchema(
            **node.model_dump(),
            **attributes.model_dump(),
            holder=attribute_type.holder,
        )

    async def __get_root_node_id(self, node_id: NodeId) -> NodeId:
        """
        get root node id of a given node

        Args:
            node_id (str): id of node whose root you are seeking

        Returns:
            str: id of root node

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        node = await self.__get(node_id)
        while node.parent is not None:
            node = await self.__get(node.parent)
        return node.id

    async def delete(self, node_id: NodeId) -> None:
        """
        Deletes node

        Args:
            node_id (str): id of a node to be deleted

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        node = await self.__get(node_id)
        if node.parent is not None:
            parent = await self.__get(node.parent)
            parent.children.remove(node_id)
            self.__registry.update(parent.id, parent.model_dump(exclude={"id"}))

        children = [node_id]
        while len(children) > 0:
            node_id = children.pop()
            try:
                node = await self.__get(node_id)
            except NodeNotFoundError:
                continue
            children.extend(node.children)
            self.__registry.delete(node_id)
            await self.__attribute_service.delete_attribute(node_id)

    async def __reparent(self, node_id: NodeId, new_parent_id: NodeId) -> None:
        """
        change parent of node with new_parent_id

        Args:
            node_id (str): node to change parent id
            new_parent_id (str): new parent id

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        node = await self.__get(node_id)
        parent = await self.__get(new_parent_id)
        if node.parent is not None:
            old_parent = await self.__get(node.parent)
            old_parent.children.remove(node.id)
            self.__registry.update(old_parent.id, old_parent.model_dump(exclude={"id"}))

        parent.children.append(node.id)
        node.parent = parent.id

        self.__registry.update(node.id, node.model_dump(exclude={"id"}))
        self.__registry.update(parent.id, parent.model_dump(exclude={"id"}))

    async def __check_initiator_permission(
        self, initiator_id: UserId, node_id: NodeId
    ) -> None:
        """
        Check if initiator can manipulate with node pointed by node_id

        Args:
            initiator_id (str): id of user who initiates action
            node_id (str): id of node which will be used

        Raises:
            NotAllowedError: raised when initiator can't performe actions with node
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        root_node_id = await self.__get_root_node_id(node_id)
        project = await self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

    async def __change_position(self, node_id: NodeId, new_position: int) -> None:
        node = await self.__get(node_id)
        if node.parent is None:
            raise IncompatibleNodeError
        parent_node = await self.__get(node.parent)
        parent_node.children.remove(node.id)
        parent_node.children.insert(new_position, node.id)
        self.__registry.update(parent_node.id, {"children": parent_node.children})

    async def __in_same_tree(self, *node_ids: NodeId) -> bool:
        """
        Check if all node_id located in same tree.

        Args:
            node_ids (tuple[NodeId]): ids of nodes to check

        Returns:
            bool: True if node_ids is empty or contains only 1 node_id \
                or all nodes located is same tree, False overwhise

        Raises:
            NodeNotFoundError: raised if some node_id not exist
        """
        if len(node_ids) == 0:
            return True
        first_parent_id = await self.__get_root_node_id(node_ids[0])
        for node_id in node_ids[1:]:
            current_parent_id = await self.__get_root_node_id(node_id)
            if current_parent_id != first_parent_id:
                return False
        return True
