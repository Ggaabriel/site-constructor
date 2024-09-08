from abc import ABC, abstractmethod
from typing import Optional

from ..RegistryTypes import RegistryData, RegistryQuery


class IRegistry(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def create(self, id: str, data: RegistryData) -> None:
        pass

    @abstractmethod
    def read(self, query: RegistryQuery) -> list[RegistryData]:
        pass

    @abstractmethod
    def update(self, id: str, data: RegistryData) -> bool:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[RegistryData]:
        pass
