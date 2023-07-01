from pydantic import BaseModel, Field


# Схема, которую нужно будет заполнить пользователю, чтобы авторизироваться.
class UserLogin(BaseModel):
    login: str = Field(default=None)
    password: str = Field(default=None)
