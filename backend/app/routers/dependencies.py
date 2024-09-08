import hashlib
import hmac
import json
from json import JSONDecodeError
from typing import Annotated
from urllib.parse import unquote

from fastapi import Depends, Header, HTTPException, status

from app.config import settings
from app.registry import IRegistryFactory, RegistryFactory
from app.services import ServiceMediator
from app.services.AttributeService.IAttributeService import IAttributeService
from app.services.HTMLService import IHTMLService
from app.services.ImageService import IImageService
from app.services.NodeService import INodeService
from app.services.ProjectService import IProjectService
from app.services.TemplateService.ITemplateService import ITemplateService
from app.services.UserService import IUserService
from app.services.UserService.schemas.UserId import UserId

secret_key = hmac.new(
    "WebAppData".encode("utf-8"), settings.bot_key.encode("utf-8"), hashlib.sha256
).digest()
service_mediator: ServiceMediator | None = None
registry_factory: IRegistryFactory | None = None


async def get_registry_factory() -> IRegistryFactory:
    global registry_factory
    if registry_factory is None:
        registry_factory = RegistryFactory()
    return registry_factory


async def get_service_mediator(
    registry_factory: Annotated[IRegistryFactory, Depends(get_registry_factory)]
) -> ServiceMediator:
    global service_mediator
    if service_mediator is None:
        service_mediator = ServiceMediator(registry_factory)
    return service_mediator


async def get_user_service(
    service_mediator: Annotated[ServiceMediator, Depends(get_service_mediator)]
) -> IUserService:
    return await service_mediator.get_user_service()


async def get_project_service(
    service_mediator: Annotated[ServiceMediator, Depends(get_service_mediator)]
) -> IProjectService:
    return await service_mediator.get_project_service()


async def get_node_service(
    service_mediator: Annotated[ServiceMediator, Depends(get_service_mediator)]
) -> INodeService:
    return await service_mediator.get_node_service()


async def get_template_service(
    service_mediator: Annotated[ServiceMediator, Depends(get_service_mediator)]
) -> ITemplateService:
    return await service_mediator.get_template_service()


async def get_attributes_service(
    service_mediator: Annotated[ServiceMediator, Depends(get_service_mediator)]
) -> IAttributeService:
    return await service_mediator.get_attribute_service()


async def get_image_service(
    service_mediator: Annotated[ServiceMediator, Depends(get_service_mediator)]
) -> IImageService:
    return await service_mediator.get_image_service()


async def get_html_service(
    service_mediator: Annotated[ServiceMediator, Depends(get_service_mediator)]
) -> IHTMLService:
    return await service_mediator.get_html_service()


async def get_user_id_by_init_data(user_init_data: Annotated[str, Header()]) -> UserId:
    init_data_dict = await parse_to_dict(user_init_data)
    if settings.mode != "local" and not await verify(init_data_dict):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Telegram token")
    try:
        user_id: int = json.loads(init_data_dict["user"])["id"]
    except JSONDecodeError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid Telegram token format"
        )
    return UserId(str(user_id))


async def parse_to_dict(init_data: str) -> dict[str, str]:
    chunks = unquote(init_data).split("&")
    chunk_dict = dict()
    for chunk in chunks:
        splitted = chunk.split("=")
        if len(splitted) != 2:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Invalid Telegram token format"
            )
        chunk_dict[splitted[0]] = splitted[1]
    return chunk_dict


async def verify(init_data_dict: dict[str, str]) -> bool:
    hash = init_data_dict.get("hash", None)
    if hash is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid Telegram token format"
        )
    pairs = [f"{key}={value}" for key, value in init_data_dict.items() if key != "hash"]
    pairs.sort()
    data_paired = "\n".join(pairs)
    self_hashed = hmac.new(
        secret_key, data_paired.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return hash == self_hashed
