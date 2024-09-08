from pydantic import BaseModel

from .types import AttributeTypeId


class NodeAttributeExternalSchema(BaseModel):
    type_id: AttributeTypeId
    attrs: dict[str, str]
