# from asyncio import run, gather
from uvicorn import run

from init import db

from fastapi import FastAPI
from routers.organization import organization

app = FastAPI()
app.include_router(organization)

# async def init():
#     is_table: bool = await db.create_table()
#     if not is_table:
#         return False

#     insert_organization: bool = await db.insert_test_organization()


if __name__ == "__main__":
    # run(init())
    run("main:app")