from src.exceptions.base_exceptions import AppException
from pydantic import BaseModel
from src.schemas.base_schemas import BaseSchema


def add_internal_params(schema, cls_internal, raise_exception: bool = True, **params):
    import sqlalchemy.engine.row as sql_row
    if not isinstance(cls_internal, type):
        cls_internal = cls_internal.__class__

    new_model = cls_internal.model_construct()

    if schema is None:
        pass

    elif isinstance(schema, BaseModel):
        for key, value in schema.__dict__.items():
            if key in new_model.model_fields:
                setattr(new_model, key, value)
            elif raise_exception:
                raise AppException(400, f"cls {cls_internal} has not parameter {key} from model {schema.__class__}")

    elif isinstance(schema, sql_row.Row):
        for key, value in schema._asdict().items():
            if key in new_model.model_fields:
                setattr(new_model, key, value)
            elif raise_exception:
                raise AppException(400, f"cls {cls_internal} has not parameter {key}")
    else:
        raise AppException(400, f"schema {schema} is not instance of BaseModel or sql.row, Its {type(schema)}")

    for key, value in params.items():
        if key in new_model.model_fields:
            setattr(new_model, key, value)
        elif raise_exception:
            raise AppException(400, f"cls {cls_internal} has not parameter {key}")

    return new_model


def delete_none_params(schema):
    for key in list(schema.__dict__.keys()):
        if getattr(schema, key) is None:
            delattr(schema, key)


def get_selected_columns(schema: type[BaseSchema], cls_model: type[BaseModel]):
    """Возвращает только нужные колонки из ORM-модели, основываясь на Pydantic-модели"""
    selected_items = schema.model_fields
    return [getattr(cls_model, column) for column in selected_items if hasattr(cls_model, column)]
