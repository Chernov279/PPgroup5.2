import pytest

from src.exceptions.base_exceptions import AppException
from src.schemas.base_schemas import BaseSchema
from src.utils.schema_utils import add_internal_params, delete_none_params, get_selected_columns
from tests.pytest_fixtures import SchemaInternal, sample_internal, sample_schema, SomeSchema


# Тест успешного добавления параметров
def test_add_internal_params_valid(sample_schema):
    result = add_internal_params(sample_schema, SchemaInternal)
    assert result.id == 1
    assert result.name == "Test User"
    assert result.age == 25


def test_add_internal_params_invalid_key(sample_internal, sample_schema):
    with pytest.raises(AppException, match="cls .* has not parameter age"):
        add_internal_params(sample_internal, SomeSchema)
    with pytest.raises(AppException) as exc_info:
        add_internal_params(sample_schema, SchemaInternal, extra_param="invalid")
    assert "has not parameter extra_param" in str(exc_info.value)


# Тест обработки schema = None (должен просто вернуть пустой объект SchemaInternal)
def test_add_internal_params_none_schema():
    result = add_internal_params(None, SchemaInternal)
    assert isinstance(result, SchemaInternal)


# Тест обработки неверного типа schema
def test_add_internal_params_invalid_schema():
    with pytest.raises(AppException) as exc_info:
        add_internal_params({}, SchemaInternal)  # Словарь вместо объекта Pydantic

    assert "is not instance of BaseModel or sql.row" in str(exc_info.value)


# Тест удаления None-полей
def test_delete_none_params():
    class TestModel(BaseSchema):
        id: int
        name: str | None

    obj = TestModel(id=1, name=None)
    delete_none_params(obj)
    assert not hasattr(obj, "name")  # Поле должно быть удалено


# Тест получения колонок ORM-модели по Pydantic-схеме
def test_get_selected_columns():
    class ORMModel:
        id = "id_col"
        name = "name_col"
        age = "age_col"

    class Schema(BaseSchema):
        id: int
        name: str

    result = get_selected_columns(Schema, ORMModel)
    assert result == ["id_col", "name_col"]
