from typing import Any, Optional

from ..IRegistry import IRegistry
from ..RegistryTypes import RegistryData, RegistryQuery


class DynamoRegistry(IRegistry):
    __table: Any

    def __init__(self, table: Any) -> None:
        super().__init__()
        self.__table = table

    def create(self, id: str, data: RegistryData) -> None:
        if "id" in data:
            raise AttributeError("Key 'id' can not be in data attribute")
        data["id"] = id
        self.__table.put_item(Item=data)

    def read(self, query: RegistryQuery) -> list[RegistryData]:
        response = self.__table.scan(
            ScanFilter={
                key: {"AttributeValueList": [value], "ComparisonOperator": "EQ"}
                for key, value in query.items()
            }
        )
        return response["Items"]

    def update(self, id: str, data: RegistryData) -> bool:
        if "id" in data:
            raise AttributeError("Key 'id' can not be in data attribute")
        response = self.__table.update_item(
            Key={"id": id},
            AttributeUpdates={
                key: {"Value": value, "Action": "PUT"} for key, value in data.items()
            },
            ReturnValues="ALL_OLD",
        )
        return "id" in response["Attributes"]

    def delete(self, id: str) -> bool:
        response = self.__table.delete_item(
            Key={"id": id},
            ReturnValues="ALL_OLD",
        )
        return "id" in response["Attributes"]

    def get(self, id: str) -> Optional[RegistryData]:
        response: dict[str, Any] = self.__table.get_item(Key={"id": id})
        # raise ValueError(response)
        return response.get("Item", None)
