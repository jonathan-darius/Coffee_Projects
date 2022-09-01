from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.model import mongo
from app.scheme import mongo as models

app = APIRouter()


@app.get("/all_user")
def get_data():
    return mongo.get_all_user()


@app.post("/Register")
def register(user: models.UserModel = Body(...)):
    return mongo.register_user(user)


@app.post("/Login")
def login(log: OAuth2PasswordRequestForm = Depends()):
    return mongo.login_user(log)
