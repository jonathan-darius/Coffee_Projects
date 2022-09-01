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


class Settings(CommonSetting, ServerSetting, DatabaseSettings, ElasticSetting):
    pass


settings = Settings()
