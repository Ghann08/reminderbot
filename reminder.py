import asyncio
from ast import increment_lineno
from json import dumps, loads
from dateutils import relativedelta
import datetime
import re
from uuid import UUID, uuid4

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from telegram.ext import ContextTypes
from pydantic import BaseModel
from typing import Optional, Awaitable, Callable

class Answer:
    text: str
    reply_markup: InlineKeyboardMarkup

    def __init__(self, text: str, reply_markup: list):
        self.text = text
        self.reply_markup = reply_markup


class Reminder:
    text: str
    id: UUID
    _last_generated_month: datetime.date
    selected_date: datetime.date
    selected_time: datetime.time
    _on_delete: Callable[[UUID], Awaitable[None]]
    calendry = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь",
                "декабрь"]

    def __init__(self, on_delete: Callable[[UUID], Awaitable[None]]):
        self.text = None
        self.id = uuid4()
        self._last_generated_month = datetime.date.today()
        self.selected_date = None
        self.selected_time = None
        self._on_delete = on_delete

    def change_month(self, delta: int):
        self._last_generated_month += relativedelta(months=delta)

    def generate_week(self, first_date: datetime.datetime):
        for c in range(7):
            date = first_date + datetime.timedelta(days=c)
            yield InlineKeyboardButton(text=str(date.day), callback_data=date.date().isoformat())


    def generate_month(self):
        month = self._last_generated_month.month
        year = self._last_generated_month.year
        first_day_week_day = datetime.datetime.weekday(datetime.datetime(year, month, 1))
        generate_day_from = datetime.datetime(year, month, 1) - datetime.timedelta(first_day_week_day)

        yield [x for x in self.generate_week(generate_day_from)]
        generate_day_from = generate_day_from + datetime.timedelta(days=7)
        while generate_day_from.month == month:
            yield [x for x in self.generate_week(generate_day_from)]
            generate_day_from = generate_day_from + datetime.timedelta(days=7)

        yield [InlineKeyboardButton(" <<< ", callback_data='minus_month')
                if self._last_generated_month > datetime.date.today() else \
                    InlineKeyboardButton(" ", callback_data='skip_any'),
               InlineKeyboardButton(f'{self.calendry[month - 1]} ({self._last_generated_month.year})' , callback_data='skip_any'),
               InlineKeyboardButton(" >>> ", callback_data='plus_month')]


    async def remind(self, message: Message):
        number_even_numbers = 0
        time = datetime.datetime.now()
        for i in range(time.month, self.selected_date.month):
            if i % 2 == 0:
                number_even_numbers += 1
        dayinsec = (((self.selected_date.month - time.month) * 30 + number_even_numbers) - time.day + self.selected_date.day) * 86400
        hourinsec = ((self.selected_time.hour - datetime.datetime.now().time().hour) * 3600)
        mininsec = (self.selected_time.minute - datetime.datetime.now().time().minute) * 60
        x = (dayinsec + hourinsec + mininsec) - datetime.datetime.now().time().second
        await asyncio.sleep(x)
        await message.reply_text(text=self.text)


class User:
    reminders: dict[UUID, Reminder]
    current_reminder: Reminder
    _user_id: int

    def __init__(self, user_id: int):
        self._user_id = user_id
        self.current_reminder = None
        self.reminders = {}

    async def delete_remind(self, remind_id: UUID):
        pass

    def try_parce_time(self, user_input: str):
        user_input = user_input.strip().lower()

        # 1. HH:MM or H:MM
        match = re.search(r'(\d{1,2})[:.](\d{2})', user_input)
        if match:
            h, m = int(match[1]), int(match[2])
            if 0 <= h < 24 and 0 <= m < 60:
                return datetime.time(h, m)

        # 2. H[am|pm]
        match = re.search(r'(\d{1,2})\s?(am|pm)', user_input)
        if match:
            h = int(match[1])
            if match[2] == 'pm' and h != 12:
                h += 12
            if match[2] == 'am' and h == 12:
                h = 0
            return datetime.time(h, 0)

        # 3. Just hour
        match = re.search(r'\b(\d{1,2})\b', user_input)
        if match:
            h = int(match[1])
            if 0 <= h < 24:
                return datetime.time(h, 0)

        return None

    async def process_message(self, message: Message):
        if self.current_reminder is None:
            self.current_reminder = Reminder(self.delete_remind)

        # Если мы только создали напоминальщик, то мы хотим записать текст
        # и вернуть нам надо календарик
        if self.current_reminder.text is None:
            self.current_reminder.text = message.text
            return Answer('Когда отравить?', InlineKeyboardMarkup([x for x in self.current_reminder.generate_month()]))

        # если текст уже задан, то мы в тексте можем только время получить
        # попытаемся распарсить
        # если поулчилось, то значит мы выполнили все условия
        # отправка
        else:
            tm = self.try_parce_time(message.text)
            if tm is None:
                self.current_reminder = None
                return Answer('Неправильное время', None)
            elif tm.hour < datetime.datetime.now().hour:
                self.current_reminder = None
                return Answer('Неправильное время', None)
            elif tm.minute < datetime.datetime.now().minute and tm.hour == datetime.datetime.now().hour:
                self.current_reminder = None
                return Answer('Неправильное время', None)
            else:
                self.current_reminder.selected_time = tm
                asyncio.create_task(self.current_reminder.remind(message))
                self.reminders[self.current_reminder.id] = self.current_reminder
                res = Answer(f'Напомним вам: {self.current_reminder.selected_date} в {self.current_reminder.selected_time}', None)
                self.current_reminder = None
                return res



    async def process_button(self, message: CallbackQuery):
        if self.current_reminder is None:
            raise Exception('Impossible!')
        # Если нажали кнопку, то это календарь
        # если "plus_month" или "minus_month" - то перещёлкивание месяца, иначе выбрали дату
        if message.data == 'plus_month':
            self.current_reminder.change_month(1)
            return Answer('Когда отравить?', InlineKeyboardMarkup([x for x in self.current_reminder.generate_month()]))
        elif message.data == 'minus_month':
            self.current_reminder.change_month(-1)
            return Answer('Когда отравить?', InlineKeyboardMarkup([x for x in self.current_reminder.generate_month()]))
        elif datetime.date.fromisoformat(message.data).day < datetime.datetime.now().date().day and datetime.date.fromisoformat(message.data).month <= datetime.datetime.now().date().month:
            return Answer('Когда отравить?', InlineKeyboardMarkup([x for x in self.current_reminder.generate_month()]))
        elif datetime.date.fromisoformat(message.data).month < datetime.datetime.now().date().month:
            return Answer('Когда отравить?', InlineKeyboardMarkup([x for x in self.current_reminder.generate_month()]))

            # todo: далёкое туду, учесть, что юзер может выбрать дату сегодня и ждать до завтра. Надо бы взводить таймер.
        else:
            try:
                self.current_reminder.selected_date = datetime.date.fromisoformat(message.data)
                return Answer('''Теперь введите время
            Часы:Минуты''' , None)
            except ValueError:
                pass
                # считаем, что это нажата кнопка "месяца"




user_data: dict[int, User] = {}


async def rem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id not in user_data:
        user_data[update.message.chat_id] = User(update.message.chat_id)

    user = user_data[update.message.chat_id]
    ans = await user.process_message(update.message)
    await update.message.reply_text(ans.text, reply_markup=ans.reply_markup)

async def send_remind(text: str):
    pass

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = user_data[update.callback_query.message.chat_id]
    ans = await user.process_button(update.callback_query)
    await update.callback_query.edit_message_text(ans.text, reply_markup=ans.reply_markup)

# todo: оформить выбор времени напоминания
# todo офрмить сохраиеие напоминаний при выключение и старта сервиса
# todo офрмить логирование запросов
# todo баг со временем(не правильно посчитал количество днеё до 29   июля, проблема с чётными месецами
