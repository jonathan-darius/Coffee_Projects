from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.model import mongo
from app.scheme import mongo as models
from app.utils.deps import get_current_user

app = APIRouter()


@app.post("/Register")
def register(user: models.UserModel = Body(...)):
    return mongo.register_user(user)


@app.post("/Login")
def login(log: OAuth2PasswordRequestForm = Depends()):
    return mongo.login_user(log)


@app.get("/all_user")
def get_data():
    return mongo.get_all_user()


@app.get('/me', summary='Get details of currently logged in user')
async def get_me(user=Depends(get_current_user)):
    return user
