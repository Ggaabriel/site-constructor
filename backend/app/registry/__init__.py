from .DynamoRegistry import DynamoRegistryFactory
from .IRegistry import IRegistry, IRegistryFactory

RegistryFactory = DynamoRegistryFactory

__all__ = [
    "IRegistry",
    "IRegistryFactory",
    "RegistryFactory",
]
