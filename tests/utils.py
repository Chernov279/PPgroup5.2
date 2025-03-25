from typing import Type, List, Any
from pydantic import BaseModel

from tests.default_test_data import DEFAULT_TEST_DATA


def generate_test_objects(
    cls: Type[BaseModel],
    count: int = 1,
    cycle_data: bool = True,
    **custom_params: List[Any]
):
    """
    Функция для генерации тестовых объектов Pydantic-схемы.

    cls: Класс Pydantic, который нужно заполнить тестовыми данными.
    count: Количество объектов для генерации.
    cycle_data: Если True, default_test_data будут зацикливаться, если их меньше, чем count.
    custom_params: Пользовательские параметры, если нужны конкретные значения.
    Количество значений должно совпадать с величиной count

    :return: Список объектов указанного класса.
    """
    schema_fields = cls.model_fields.keys()

    prepared_data = {key: None for key in schema_fields}

    for field in schema_fields:
        if field in custom_params:
            field_data = custom_params[field]
        else:
            field_data = DEFAULT_TEST_DATA.get(field, [None] * count)

        if cycle_data:
            prepared_data[field] = (field_data * ((count // len(field_data)) + 1))[:count]
        else:
            if count > len(field_data):
                prepared_data[field] = field_data + [None] * (count - len(field_data))
            else:
                prepared_data[field] = field_data
    result_objects = [
        cls(**{field: prepared_data[field][i] for field in schema_fields})
        for i in range(count)
    ]

    return result_objects
