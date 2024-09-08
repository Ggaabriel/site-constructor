from abc import ABC, abstractmethod
from re import Pattern

from .IFileWrapper import IFileWrapper


class IFileService(ABC):

    @abstractmethod
    async def add_file(
        self,
        file: IFileWrapper,
        allowed_formats: Pattern,
        file_name: str,
    ) -> None:
        pass

    @abstractmethod
    async def remove_file(self, file_name: str) -> None:
        pass

    @abstractmethod
    async def create_folder(self, folder_path: str, folder_name: str) -> None:
        pass

    @abstractmethod
    async def remove_folder(self, folder_path: str) -> None:
        pass

    @abstractmethod
    async def save_page(self, path: str, html: str) -> None:
        pass

    @abstractmethod
    async def exists(self, file_path: str) -> bool:
        pass
