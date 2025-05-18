from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from typing import AsyncIterator
import uvicorn
from pydantic import BaseModel
import asyncio
from asyncio import create_task





# Логика для lifespan (запуск/остановка)
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.post("/items/")
async def remind(tm_diff: int, text: str) -> dict:
    await asyncio.sleep(tm_diff)
    print(text)
    return {"e": "okey"}


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000)
