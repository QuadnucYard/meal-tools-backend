from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.util import greenlet_spawn


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def model_validate_async(cls, obj: Any):
        return await greenlet_spawn(lambda: cls.model_validate(obj))


class TimeMixin:
    create_time: datetime
    update_time: datetime

    @field_validator("create_time")
    def validate_create_time(cls, v: datetime):
        return v.replace(tzinfo=timezone.utc)

    @field_validator("update_time")
    def validate_update_time(cls, v: datetime):
        return v.replace(tzinfo=timezone.utc)
