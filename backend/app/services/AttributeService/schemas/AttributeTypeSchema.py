from pydantic import BaseModel, computed_field

from .types import AttributeTypeId, RegexStr


class AttributeTypeSchema(BaseModel):
    id: AttributeTypeId
    attrs: dict[str, RegexStr]

    @computed_field  # type: ignore
    @property
    def holder(self) -> bool:
        holders = ["container"]
        if self.id in holders:
            return True
        return False
