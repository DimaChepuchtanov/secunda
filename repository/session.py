from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine,
    AsyncSession
)
from setting import setting


URL = "postgresql+asyncpg://" +\
      f"{setting.PG_USER}:{setting.PG_PASSWORD}" +\
      "@" +\
      f"{setting.PG_HOST}:{setting.PG_PORT}" +\
      "/" +\
      f"{setting.PG_DB}"


class LocalSessionPG:
    def __init__(self):
        self.engine = create_async_engine(url=URL)
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        self.session = None

    async def __aenter__(self):
        self.session = self.sessionmaker()
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        try:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
        finally:
            await self.session.close()