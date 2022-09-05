from uuid import uuid4
from pydantic import BaseModel, Field, validator, EmailStr
from app.utils.hash import is_hash, hash_password
from app.config import mongo
from datetime import date
from typing import Optional


class UserModel(BaseModel):
    id_user: str = Field(default_factory=uuid4, alias="_id")
    name: str = Field(...)
    address: str = Field(...)
    email: EmailStr = Field(...)
    role: list = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    status: bool = Field(True)

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

    @validator('role')
    def role_standart(cls, roles: list):
        if len(roles) == 0:
            raise ValueError("Invalid Role")
        for i, x in enumerate(roles):
            roles[i] = x.capitalize()
            if roles[i] not in ["Farmer", "Collector", "Roaster", "Processor", "Cafe"]:
                raise ValueError("Invalid Role")
        else:
            return roles
        # return [x.capitalize() for x in roles]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "John Doe",
                "address": "Unknown Street 41B",
                "email": "JohnDoe@FakeMail.com",
                "role": ["Farmer"],
                "username": "joni",
                "password": "Fill Me ...."
            }
        }


class Collector(BaseModel):
    id_transaction: str = Field(default_factory=uuid4, alias="_id")
    farmer_name: str = Field(..., alias="farmer_id")
    collector_name: str = Field(...,alias="collector_id")
    qty: int = Field(...)
    price: int = Field(...)
    coffee_type: str = Field(...)
    send_date: date = Field(...)
    receive_date: Optional[date] = None
    address: str = Field(...)

    @validator('farmer_name')
    def cek(cls, val):
        try:
            client, data = mongo.db()
            checker = data["User"].find_one({'username': val})

            if checker is None:
                raise ValueError("User Not Found")
            else:
                if "Farmer" in checker["role"]:
                    return checker["_id"]
                else:
                    raise ValueError("Role Doesn't Match")
        except Exception as e:
            raise ValueError(e)

    @validator('collector_name')
    def check(cls, val):
        try:
            client, data = mongo.db()
            checker = data["User"].find_one({'username': val})

            if checker is None:
                raise ValueError("Not Found")
            else:
                if "Collector" in checker["role"]:
                    return checker["_id"]
                else:
                    raise ValueError("Role Doesn't Match")
        except Exception as e:
            raise ValueError(e)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "farmer_name": "joni",
                "collector_name": "john Doe",
                "qty": "5",
                "price": "5",
                "coffee_type": "Robusta",
                "send_date": "22102022",
                "address": "Unknown Street 41B"
            }
        }
