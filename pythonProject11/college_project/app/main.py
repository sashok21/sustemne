from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.models.base import BaseModel

from .core.settings.db import Database

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

db = Database(url=DATABASE_URL)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    print("Database connecting...")
    await db.connect()

    async with db.engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.create_all)

    print("Database connected and tables created.")
    yield

    print("Database disconnecting...")
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get(path="/health", tags=["System"])
async def health():
    ok = await db.ping()
    return {"status": "ok"} if ok else {"status": "error"}