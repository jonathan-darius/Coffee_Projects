import traceback
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from app.config import mongo
from app.utils.hash import verify_password


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
    res = data["User"].insert_one(jsonable_encoder(usr))
    check_user = data["User"].find_one({"_id": res.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=check_user)


def login_user(login_data):
    client, data = mongo.db()
    username = login_data.username
    password = login_data.password
    user = data["User"].find_one({"username": username})
    if not user:
        return {
            "massage": "Wrong User Name or Password !!!"
        }
    return {"massage": "Login Success", "User_data": user} if verify_password(user["password"], password) else {
            "massage": "Wrong User Name or Password !!!"}
