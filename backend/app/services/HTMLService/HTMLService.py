from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app.config import settings

from ..FileService import IFileService
from ..NodeService import INodeService
from ..NodeService.schemas.NodeTreeSchema import NodeTreeSchema
from ..ProjectService import IProjectService
from ..ProjectService.schemas.ProjectId import ProjectId
from ..UserService.schemas.UserId import UserId
from .IHTMLService import IHTMLService


class HTMLService(IHTMLService):
    """A service class responsible for managing html responses"""

    __project_service: IProjectService
    __node_service: INodeService
    __file_service: IFileService
    __templates = Environment(
        loader=FileSystemLoader(Path(Path(__file__).parent, "templates")),
        autoescape=True,
        enable_async=True,
    )

    def __init__(self) -> None:
        self.__templates.globals.setdefault("server_name", settings.server_name)

    async def inject_dependencies(
        self,
        project_service: IProjectService,
        node_service: INodeService,
        file_service: IFileService,
    ) -> None:
        """
        inject dependencies necessary for service to work

        Args:
            project_service (IProjectService): service for interactions with projects
            node_service (INodeService): service for interactions with nodes
        """
        self.__project_service = project_service
        self.__node_service = node_service
        self.__file_service = file_service

    async def render_index_page(
        self, initiator_id: UserId, project_id: ProjectId
    ) -> None:

        project = await self.__project_service.try_get(initiator_id, project_id)
        root = await self.__node_service.get_tree(project.core_node_id)

        core_node = await self.__templates.get_template(
            name=f"{str(root.type_id)}.html"
        ).render_async(
            node=root,
            node_list=await self.__return_template_list(root.children),
        )
        page = await self.__templates.get_template(
            name="base.html",
        ).render_async(project_name=project.name, core=core_node)
        await self.__file_service.save_page(str(Path(initiator_id, project_id)), page)

    async def __return_template_list(
        self, child_nodes: list[NodeTreeSchema]
    ) -> list[str]:
        """
        return list of templates as strings \
        this function is used in order to get templates of all child nodes \
        of a node

        Args:
            child_nodes (list[NodeTreeSchema]): list of NodeTreeSchema objects

        Returns:
            list[str]: list of templates as strings
        """
        template_list = list()
        for child in child_nodes:
            template_list.append(
                await self.__templates.get_template(
                    name=f"{str(child.type_id)}.html"
                ).render_async(
                    node=child,
                    node_list=await self.__return_template_list(child.children),
                )
            )
        return template_list
