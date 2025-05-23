from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncIterator
import uvicorn
import asyncio
from pydantic import BaseModel

from reminder import Reminder


class Reminders(BaseModel):
    user_id: int
    text_message: str
    dispatch_difference: int


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

async def remind(tm_diff: int, text: str):
    await asyncio.sleep(tm_diff)
    print(text)


# Логика для lifespan (запуск/остановка)
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Shutting up...")
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

@app.post("/remiders/")
async def rem(rems: Reminders):
    reminds = Reminder
    await reminds.run_message(rems.dispatch_difference, rems.text_message)



if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000)
