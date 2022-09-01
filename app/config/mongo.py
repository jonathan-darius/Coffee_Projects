import pymongo
from fastapi.exceptions import HTTPException
from fastapi import status
from app.config.configs import settings


def db():
    try:
        client = pymongo.MongoClient(settings.DB_URL)
        database = client[settings.DB_NAME]
        return client, database

    except:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Failed Connect Database")
