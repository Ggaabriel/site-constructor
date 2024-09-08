from abc import ABC, abstractmethod

from ..FileService.IFileWrapper import IFileWrapper
from ..NodeService.schemas.NodeId import NodeId


class IImageService(ABC):

    @abstractmethod
    async def add_image(self, node_id: NodeId, file: IFileWrapper) -> None:
        pass

    @abstractmethod
    async def remove_image(self, node_id: NodeId) -> None:
        pass
