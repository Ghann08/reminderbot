import asyncio
from datetime import datetime
from uuid import uuid4, UUID

class Reminders():
    text: str
    date: datetime
    id_remind: UUID

    def __init__(self, text: str | None = None, date: datetime | None = None):
        self.text = text
        self.date = date
        self.id_remind = uuid4()
        if self.text != None and self.date != None:
            tm_diff = self.date - datetime.now()
            asyncio.create_task(self.create_remind(tm_diff))
        else:
            print(self.text)
            print(self.date)
            print("okey")

    def update(self, text = None , date = None):
        if self.text != text and text != None:
            self.text = text
        if self.date != date and date != None:
            self.date = date
        if self.text != None and self.date != None:
            tm_diff = self.date - datetime.now()
            asyncio.create_task(self.create_remind(tm_diff))
        else:
            print(self.text)
            print(self.date)
            print("okey")

    async def create_remind(self, tm_diff):
        print("Напоминание создано")
        await asyncio.sleep(int(tm_diff.total_seconds()))
        print(f"Напоминание: {self.text}")
