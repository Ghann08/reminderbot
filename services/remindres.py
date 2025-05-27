import asyncio
from datetime import datetime
from uuid import uuid4, UUID

class Reminders():
    text: str
    date: datetime
    id_remind: UUID

    def __init__(self, text: str, date: datetime):
        self.text = text
        self.id_remind = uuid4()
        if self.text != None:
            asyncio.create_task(self.create_remind())
        else:
            print("okey")

    async def create_remind(self):
        print("Напоминание создано")
        tm_diff = self.date = datetime.now()
        await asyncio.sleep(5)
        print(f"Напоминание: {self.text}")
