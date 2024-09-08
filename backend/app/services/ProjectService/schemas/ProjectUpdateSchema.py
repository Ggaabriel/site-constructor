from typing import Optional

from pydantic import BaseModel


class ProjectUpdateSchema(BaseModel):
    name: Optional[str]
