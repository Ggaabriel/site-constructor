from ...AttributeService.schemas.types import AttributeTypeId
from .NodeSchema import NodeSchema


class NodeExtendedSchema(NodeSchema):
    type_id: AttributeTypeId
    attrs: dict[str, str]
    holder: bool
