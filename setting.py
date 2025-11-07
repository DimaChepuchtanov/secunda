from pydantic import BaseSettings


class Setting(BaseSettings):
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: str
    PG_DB: str


setting = Setting()
