from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config.configs import settings
from app.config import mongo
from jose import jwt
from pydantic import ValidationError
from app.scheme.token import TokenPayload

JWT_SECRET_KEY = settings.Secret
ALGORITHM = settings.Algorithm

reusable_oauth: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl="/mongo/Login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    client, data = mongo.db()

    user: Union[dict[str, Any], None] = data["User"].find_one({"username": token_data.sub})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
