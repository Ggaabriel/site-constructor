from typing import Dict, Union

RegistryValue = Union[str, int, bool, dict, list]
RegistryData = Dict[str, RegistryValue]
RegistryQuery = Dict[str, RegistryValue]
