import traceback
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException
from app.config import mongo
from app.utils.hash import verify_password
from app.utils.jwt import create_access_token, create_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_all_user():
    try:
        client, data = mongo.db()
        datas = list(data["User"].find())
        return datas
    except:
        traceback.print_exc()
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Failed get data")


def register_user(usr):
    client, data = mongo.db()
    try:
        data["User"].insert_one(jsonable_encoder(usr))
        return {"massage": "User Created"}
    except Exception as e:
        return e


def login_user(login_data):
    client, data = mongo.db()
    username = login_data.username
    password = login_data.password
    user = data["User"].find_one({"username": username})
    if not user:
        return {
            "massage": "Wrong User Name or Password !!!"
        }
    elif verify_password(user["password"], password):
        return {
            "access_token": create_access_token(user['username']),
            "refresh_token": create_refresh_token(user['username'])
        }

    else:
        var = {
            "massage": "Wrong User Name or Password !!!"
        }
        return var
