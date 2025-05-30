import asyncio
from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional
from asyncio import Task

class Reminders():
    _text: Optional[str]
    _date: Optional[datetime]
    _id_remind: UUID
    _remind: Task

    def __init__(self, text: str = None, date: datetime = None):
        self.text = text
        self.date = date
        self.id_remind = uuid4()
        self.remind = asyncio.create_task(self._remind())

    def _update(self, text: str = None ,date: datetime = None):
        if self.text != text and text is not None:
            self.text = text
        if self.date != date and date is not None and date > datetime.now():
            self.date = date

    async def _remind(self):
        while self.date is not None and datetime.now() <= self.date:
            await asyncio.sleep(1)
        print(f"Напоминание: {self.text}")
        self.remind.cancel()

    async def delete_remind(self):
        self.remind.cancel()