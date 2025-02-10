from src.exceptions.base_exceptions import AppException
from src.models.base_model import BaseModel
from src.schemas.base_schemas import BaseSchema
from src.utils.base_utils import isValidModel


def add_internal_params(model: BaseModel, cls_internal: type(BaseSchema), **params):
    isValidModel(None, model)

    new_model = cls_internal()
    for key, value in model.__dict__.items():
        if hasattr(new_model, key):
            setattr(new_model, key, value)
        else:
            raise AppException(400, f"cls{cls_internal} has not parameter {key} from model {model.__class__}")

    for key, value in params.items():
        if hasattr(new_model, key):
            setattr(new_model, key, value)
        else:
            raise AppException(400, f"cls{cls_internal} has not parameter {key}")
    return new_model


def delete_none_params(schema):
    for key in list(schema.__dict__.keys()):
        if getattr(schema, key) is None:
            delattr(schema, key)


def get_selected_columns(schema: type[BaseSchema], cls_model: type[BaseModel]):
    """Возвращает только нужные колонки из ORM-модели, основываясь на Pydantic-модели"""
    selected_items = schema.model_fields
    return [getattr(cls_model, column) for column in selected_items if hasattr(cls_model, column)]
