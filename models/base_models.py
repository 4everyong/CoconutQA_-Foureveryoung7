from typing import Optional
import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator
from constants.roles import Roles


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью совпадать с полем password")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    class Config:
        json_encoders = {
            Roles: lambda v: v.value
        }

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: List[Roles] = [Roles.USER.value]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

class FilmRequest(BaseModel):
    name: str
    imageUrl: Optional[str]=None
    price: int
    description: str
    location: str
    published: bool
    genreId: int

class FilmResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str] = None
    location: str
    published: bool
    rating: int
    genreId: int
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")
    genre: dict

    @field_validator('location')
    def validate_location(cls, value):
        allowed_values = {"MSK", "SPB"}
        if value not in allowed_values:
            raise ValueError(f"Значение поля location должно быть одним из: {allowed_values}. Текущее значение: {value}")
        return value