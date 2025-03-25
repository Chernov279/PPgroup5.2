import pytest

from src.schemas.base_schemas import BaseSchema


class SomeSchema(BaseSchema):
    id: int
    name: str


class SchemaInternal(BaseSchema):
    id: int
    name: str
    age: int = 25


@pytest.fixture
def sample_schema():
    return SomeSchema(id=1, name="Test User")


@pytest.fixture
def sample_internal():
    return SchemaInternal(id=1, name="Internal User")
