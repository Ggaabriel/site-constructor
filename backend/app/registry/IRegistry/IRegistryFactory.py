from abc import ABC, abstractmethod

from .IRegistry import IRegistry


class IRegistryFactory(ABC):
    @abstractmethod
    def get(self, name: str) -> IRegistry:
        pass
