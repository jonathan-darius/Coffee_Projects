from pydantic import BaseSettings


class CommonSetting(BaseSettings):
    APP_NAME: str = "Coffee_Project"
    DEBUG_MODE: bool = True


class ServerSetting(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "coffee_project"


class ElasticSetting(BaseSettings):
    Elastic_URL: str = ""
    Elastic_Index: str = ""


class JWT(BaseSettings):
    Secret: str = "18c9a0444a5df9b9c7ed84f96e4dc8183a536d039e58db18"
    Algorithm: str = "HS256"
    EXPIRE_MINUTES = 10
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3
    REFRESH_SECRET_KEY: str = "awd12131ada"


class Settings(CommonSetting, ServerSetting, DatabaseSettings, ElasticSetting, JWT):
    pass


settings = Settings()
