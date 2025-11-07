from uvicorn import run
from fastapi import FastAPI

from repository.session import LocalSessionPG
from repository.model import Base
from router.incident import incident


app = FastAPI()
app.include_router(incident)


@app.on_event("startup")
async def create_db():
    engine = LocalSessionPG().engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    run("main:app")
