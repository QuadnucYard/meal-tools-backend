from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_validator


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimeMixin:
    create_time: datetime
    update_time: datetime

    @field_validator("create_time")
    def validate_create_time(cls, v: datetime):
        return v.replace(tzinfo=timezone.utc)

    @field_validator("update_time")
    def validate_update_time(cls, v: datetime):
        return v.replace(tzinfo=timezone.utc)
