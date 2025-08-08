from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True,
        validate_assignment=True,
    )


class MetaDataSchema(BaseSchema):
    created_at: datetime = Field(
        ..., description="Creation timestamp in ISO 8601 format",
        examples=["2023-10-05T14:48:00.000Z"])
    updated_at: datetime = Field(
        ..., description="Last update timestamp in ISO 8601 format",
        examples=["2023-10-05T14:48:00.000Z"])
