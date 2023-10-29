from pydantic import BaseModel, Field


class PageParams(BaseModel):
    sort_by: str | None = Field(default=None, description="Key on sorting")
    desc: bool = Field(default=False, description="Whether descending")
