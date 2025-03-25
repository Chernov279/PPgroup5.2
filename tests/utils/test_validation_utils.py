import pytest
from src.exceptions.base_exceptions import ValidationException
from src.models.models import User
from src.schemas.base_schemas import BaseSchema
from src.utils.base_utils import is_valid_model, is_valid_schema, has_attr_order, isValidFilters


class InvalidModel:
    id = 1


class ValidSchema(BaseSchema):
    id: int
    name: str


class InvalidSchema:
    id: int


@pytest.fixture
def valid_model():
    return User


@pytest.fixture
def invalid_model():
    return InvalidModel


@pytest.fixture
def valid_schema():
    return ValidSchema


@pytest.fixture
def invalid_schema():
    return InvalidSchema()


def test_is_valid_model(valid_model):
    is_valid_model(model=valid_model)


def test_is_valid_model_invalid(invalid_model):
    with pytest.raises(ValidationException, match="is not subclass of BaseModel"):
        is_valid_model(model=invalid_model)


def test_is_valid_schema(valid_model, valid_schema):
    is_valid_schema(model=valid_model, schema=valid_schema)  # Не должно вызывать исключение


def test_is_valid_schema_invalid(invalid_schema):
    with pytest.raises(ValidationException, match="is not subclass of BaseSchema"):
        is_valid_schema(schema=invalid_schema)


def test_is_valid_schema_missing_attr(valid_model):
    class SchemaWithExtraField(BaseSchema):
        id: int
        extra_field: str | None = None

    with pytest.raises(ValidationException, match="does not have attribute 'extra_field'"):
        is_valid_schema(model=valid_model, schema=SchemaWithExtraField(id=1))


def test_has_attr_order(valid_model):
    has_attr_order(valid_model, "id")  # Не должно вызывать исключение


def test_has_attr_order_invalid(valid_model):
    with pytest.raises(ValueError, match="is not a valid attribute"):
        has_attr_order(valid_model, "non_existing_field")


def test_isValidFilters(valid_model):
    filters = {"id": 1, "name": "test"}
    isValidFilters(valid_model, filters)  # Не должно вызывать исключение


def test_isValidFilters_invalid(valid_model):
    filters = {"non_existing_field": "value"}
    with pytest.raises(ValidationException, match="Invalid filter keys"):
        isValidFilters(valid_model, filters)