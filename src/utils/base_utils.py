from src.exceptions.base_exceptions import ValidationException
from src.models.base_model import BaseModel
from src.schemas.base_schemas import BaseSchema


def isValidModel(self=None, model=None):
    if not isinstance(model, type):
        model = model.__class__
    if not model or not issubclass(model, BaseModel):
        raise ValidationException(
            f'{self.__class__.__name__}',
            f"model: {model.__name__} - is not subclass of BaseModel or model is empty"
        )


def isValidSchema(self=None, model=None, schema=None):
    if not isinstance(schema, type):
        schema = schema.__class__
    if not schema or not issubclass(schema, BaseSchema):
        raise ValidationException(
            f'{self.__class__.__name__}',
            f"schema: {schema.__name__} - is not subclass of BaseSchema or schema is empty"
        )
    if model is None:
        return
    for attr in schema.__annotations__.keys():
        if not hasattr(model, attr):
            raise ValidationException(
                f'{self.__class__.__name__}',
                f"model: {model.__name__} does not have attribute '{attr}'"
            )



def hasAttrOrder(model, order):
    if order is not None:
        if hasattr(model, order):
            return
    raise ValueError(f"{order} is not a valid attribute of the model {model.__name__}.")


def isValidFilters(model, filters: dict):
    """
    Проверяет, что все ключи в фильтрах являются валидными атрибутами модели.
    """
    if not filters:
        return

    model_columns = {column.name for column in model.__table__.columns}
    invalid_keys = [key for key in filters if key not in model_columns]

    if invalid_keys:
        raise ValidationException(
            field=f"Filters for model {model.__name__}",
            message=f"Invalid filter keys: {', '.join(invalid_keys)}"
        )
