from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4

class Reminders(BaseModel):
    text: str | None = None
    select_date: datetime.date | None = None
    select_time: datetime.time | None = None
    id_user: uuid4
    id_remind: uuid4
