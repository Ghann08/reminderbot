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
            asyncio.get_event_loop().create_task(create_remind(self.text))
        else:
            print("okey")

async def create_remind(text):
    print("sdsds")
    await asyncio.sleep(5)
    print(text)
