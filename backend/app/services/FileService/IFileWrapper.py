from abc import ABC, abstractmethod
from typing import BinaryIO


class IFileWrapper(ABC):

    @abstractmethod
    async def read(self) -> bytes:
        pass

    @property
    @abstractmethod
    def content_type(self) -> str | None:
        pass

    @property
    @abstractmethod
    def filename(self) -> str | None:
        pass

    @property
    @abstractmethod
    def file(self) -> BinaryIO:
        pass
