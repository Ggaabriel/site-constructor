from app.registry import IRegistryFactory

from .AttributeService import IAttributeService
from .AttributeService.AttributeService import AttributeService
from .FileService.FileService import FileService
from .HTMLService import IHTMLService
from .HTMLService.HTMLService import HTMLService
from .ImageService import IImageService
from .ImageService.ImageService import ImageService
from .NodeService import INodeService
from .NodeService.NodeService import NodeService
from .ProjectService import IProjectService
from .ProjectService.ProjectService import ProjectService
from .TemplateService.ITemplateService import ITemplateService
from .TemplateService.TemplateService import TemplateService
from .UserService import IUserService
from .UserService.UserService import UserService


class ServiceMediator:
    __registry_factory: IRegistryFactory
    __user_service: UserService
    __project_service: ProjectService
    __node_service: NodeService
    __template_service: TemplateService
    __attribute_service: AttributeService
    __file_service: FileService
    __image_service: ImageService
    __html_service: HTMLService
    __dependencies_injected: bool = False

    def __init__(self, registry_factory: IRegistryFactory) -> None:
        self.__registry_factory = registry_factory
        self.__instantiate_user_service()
        self.__instantiate_file_service()
        self.__instantiate_project_service()
        self.__instantiate_node_service()
        self.__instantiate_template_service()
        self.__instantiate_attribute_service()
        self.__instantiate_image_service()
        self.__instantiate_html_service()

    async def get_user_service(self) -> IUserService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__user_service

    async def get_project_service(self) -> IProjectService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__project_service

    async def get_node_service(self) -> INodeService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__node_service

    async def get_template_service(self) -> ITemplateService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__template_service

    async def get_attribute_service(self) -> IAttributeService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__attribute_service

    async def get_image_service(self) -> IImageService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__image_service

    async def get_html_service(self) -> IHTMLService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__html_service

    async def __inject_dependencies(self) -> None:
        await self.__user_service.inject_dependencies(self.__file_service)
        await self.__project_service.inject_dependencies(
            self.__user_service,
            self.__node_service,
            self.__file_service,
        )
        await self.__node_service.inject_dependencies(
            self.__user_service,
            self.__project_service,
            self.__template_service,
            self.__attribute_service,
        )
        await self.__attribute_service.inject_dependencies(self.__file_service)
        await self.__template_service.inject_dependencies(
            self.__node_service,
        )

        await self.__image_service.inject_dependencies(
            self.__attribute_service, self.__file_service
        )

        await self.__html_service.inject_dependencies(
            self.__project_service, self.__node_service, self.__file_service
        )

    def __instantiate_user_service(self) -> None:
        users_registry = self.__registry_factory.get("users")
        self.__user_service = UserService(users_registry)

    def __instantiate_project_service(self) -> None:
        project_registry = self.__registry_factory.get("projects")
        self.__project_service = ProjectService(project_registry)

    def __instantiate_node_service(self) -> None:
        node_registry = self.__registry_factory.get("nodes")
        self.__node_service = NodeService(node_registry)

    def __instantiate_template_service(self) -> None:
        template_registry = self.__registry_factory.get("templates")
        self.__template_service = TemplateService(template_registry)

    def __instantiate_attribute_service(self) -> None:
        attribute_registry = self.__registry_factory.get("attributes")
        type_registry = self.__registry_factory.get("types")
        self.__attribute_service = AttributeService(type_registry, attribute_registry)

    def __instantiate_file_service(self) -> None:
        self.__file_service = FileService()

    def __instantiate_image_service(self) -> None:
        self.__image_service = ImageService()

    def __instantiate_html_service(self) -> None:
        self.__html_service = HTMLService()
