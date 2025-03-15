from fastapi import Query
from pydantic import field_validator

from src.schemas.base_schemas import BaseSchema
from src.utils.database_utils import valid_limit, valid_offset


class MultiGetParams(BaseSchema):
    limit: int = Query(30, description="Limit")
    offset: int = Query(0, description="Offset")

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, value):
        valid_limit(value)
        return value

    @field_validator("offset")
    @classmethod
    def validate_offset(cls, value):
        valid_offset(value)
        return value
