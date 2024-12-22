from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    login: str = Field(nullable=False)
    password: str = Field(min_length=3, max_length=64, nullable=True)


class UserSignUp(UserLogin):
    name: str = Field(min_length=3, max_length=64)
