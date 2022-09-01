from uuid import uuid4
from pydantic import BaseModel, Field, validator, EmailStr
from app.utils.hash import is_hash, hash_password
from app.config import mongo


class UserModel(BaseModel):
    id_user: str = Field(default_factory=uuid4, alias="_id")
    name: str = Field(...)
    address: str = Field(...)
    email: EmailStr = Field(...)
    role: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)

    @validator('password')
    def hash_password(cls, pw: str) -> str:
        if is_hash(pw):
            return pw
        return hash_password(pw)

    @validator('username')
    def check_username(cls, value: str) -> str:
        try:
            client, data = mongo.db()
            checker = data["User"].find_one({'username': value})
            if checker is None:
                return value
            else:
                raise ValueError("Username already used!")
        except Exception as e:
            raise ValueError(e)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "John Doe",
                "address": "Unknown Street 41B",
                "email": "JohnDoe@FakeMail.com",
                "role": "Farmer",
                "username": "joni",
                "password": "Fill Me ...."
            }
        }
