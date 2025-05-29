from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional


class Reminders(BaseModel):
    text: Optional[str] = Field(default=None, description='Текст напоминания')
    select_date: Optional[datetime.date] = Field(default=None, description='Дата напоминания')
    select_time: Optional[datetime.time] = Field(default=None, description='Время напоминания')
    id_user: Optional[UUID] = Field(description='id пользователя')
    id_remind: Optional[UUID] = Field(description='id напоминия')
