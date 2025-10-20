from pydantic import BaseSettings


class Setting(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1q2w3e4r"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "test_db"


setting = Setting()