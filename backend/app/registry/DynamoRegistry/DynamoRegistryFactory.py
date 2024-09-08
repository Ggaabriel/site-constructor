import os
from typing import Any

import boto3

from ..IRegistry import IRegistry, IRegistryFactory
from .DynamoRegistry import DynamoRegistry


class DynamoRegistryFactory(IRegistryFactory):
    __dynamodb: Any

    def __init__(self) -> None:
        super().__init__()
        endpoint = os.getenv("YDB_DOCUMENT_API_ENDPOINT")
        region = os.getenv("YDB_DOCUMENT_API_REGION", "us-east-1")
        self.__dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=endpoint,
            region_name=region,
        )

    def get(self, name: str) -> IRegistry:
        self.__create_table(name)
        return DynamoRegistry(self.__dynamodb.Table(name))

    def __create_table(self, name: str) -> None:
        if name in self.__get_table_names():
            return
        self.__dynamodb.create_table(
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            BillingMode="PAY_PER_REQUEST",
            TableName=name,
        )

    def __get_table_names(self) -> list[str]:
        return [table.table_name for table in self.__dynamodb.tables.all()]
