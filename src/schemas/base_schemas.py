from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes: True

    @classmethod
    def get_selected_columns(cls, cls_model):
        return [getattr(cls_model, column_name) for column_name in cls.model_fields.keys() if hasattr(cls_model, column_name)]
