import asyncio
from json import dumps, loads
import datetime
from yaml import safe_load



from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, MessageHandler


cfg = safe_load(open('config.yml').read())
app = Application.builder().token(cfg.get('token')).build()
user_events = {}
start_handler = None
calendry =["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
text = None
GET_RIMEND, GET_TIME = range(2)

def generate_week(first_date: datetime.datetime):
    for c in range(7):
        yield first_date + datetime.timedelta(c)


def generate_month(month: int, year: int):
    first_day_week_day = datetime.datetime.weekday(datetime.datetime(year, month, 1))
    last_day = datetime.datetime(year, month, 1) - datetime.timedelta(first_day_week_day)
    while last_day.month <= month:
        res = [x for x in generate_week(last_day)]
        last_day = res[-1] + datetime.timedelta(1)
        yield [f'{x.year}.{x.month}.{x.day}' for x in res]

async def get_time(update: Update, day: int, month: int, text: str):
    await update.callback_query.message.reply_text("""Введите время напомиания в формате:
                                            
часы.минуты""")
    print(update)

async def startrem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("dsd")
    await update.message.reply_text("введите текст напоминания")
    return GET_RIMEND


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, month: int):
    global text
    print(month)
    z = [x for x in generate_month(month, 2025)]
    print(month)
    keyboard = [
        [
            InlineKeyboardButton(z[0][day - 1].split(".")[2], callback_data=dumps(
                dict(answer="none", day=int(z[0][day - 1].split(".")[2]), month=int(z[0][day - 1].split(".")[1]), text=text),
                ensure_ascii=False))
            for num, day in enumerate([1, 2, 3, 4, 5, 6, 7])
        ],
        [
            InlineKeyboardButton(z[1][day - 8].split(".")[2], callback_data=dumps(
                dict(answer="none", day=int(z[1][day - 8].split(".")[2]), month=int(z[1][day - 8].split(".")[1]), text=text),
                ensure_ascii=False))
            for num, day in enumerate([8, 9, 10, 11, 12, 13, 14])
        ],
        [
            InlineKeyboardButton(z[2][day - 15].split(".")[2], callback_data=dumps(
                dict(answer="none", day=int(z[2][day - 15].split(".")[2]), month=int(z[2][day - 15].split(".")[1]), text=text),
                ensure_ascii=False))
            for num, day in enumerate([15, 16, 17, 18, 19, 20, 21])
        ],
        [
            InlineKeyboardButton(z[3][day - 22].split(".")[2], callback_data=dumps(
                dict(answer="none", day=int(z[3][day - 22].split(".")[2]), month=int(z[3][day - 22].split(".")[1]), text=text),
                ensure_ascii=False))
            for num, day in enumerate([22, 23, 24, 25, 26, 27, 28])
        ],
        [
            InlineKeyboardButton(z[4][day - 29].split(".")[2], callback_data=dumps(
                dict(answer="none", day=int(z[4][day - 29].split(".")[2]), month=int(z[4][day - 29].split(".")[1]), text=text),
                ensure_ascii=False))
            for num, day in enumerate([29, 30, 31, 32, 33, 34, 35])
        ],
        [
            InlineKeyboardButton(" <<< ",
                                 callback_data=dumps((dict(answer="back", day=datetime.datetime.now().day,
                                                           month=month)))),
            InlineKeyboardButton(calendry[month - 1],
                                 callback_data=dumps((dict(answer="none", day=datetime.datetime.now().day,
                                                           month=month)))),
            InlineKeyboardButton(" >>> ",
                                 callback_data=dumps((dict(answer="forward", day=datetime.datetime.now().day,
                                                           month=month))))
        ]
    ]

    await update.callback_query.message.reply_text("Через сколько минут напомнить?", reply_markup=InlineKeyboardMarkup(keyboard))

async def rem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global text
    month = datetime.datetime.now().month
    z =  [x for x in generate_month(month, 2025)]
    print("sdsd")
    text = update.message.text
    keyboard = [
        [
            InlineKeyboardButton(z[0][day-1].split(".")[2], callback_data=dumps(dict(answer="none", day=int(z[0][day-1].split(".")[2]), month = int(z[0][day-1].split(".")[1]), text=text), ensure_ascii=False))
            for num, day in enumerate([1, 2, 3, 4, 5, 6, 7])
        ],
        [
            InlineKeyboardButton(z[1][day-8].split(".")[2], callback_data=dumps(dict(answer="none", day=int(z[1][day-8].split(".")[2]), month = int(z[1][day-8].split(".")[1]), text=text), ensure_ascii=False))
            for num, day in enumerate([8, 9, 10, 11, 12, 13, 14])
        ],
        [
            InlineKeyboardButton(z[2][day-15].split(".")[2], callback_data=dumps(dict(answer="none", day=int(z[2][day-15].split(".")[2]), month = int(z[2][day-15].split(".")[1]), text=text), ensure_ascii=False))
            for num, day in enumerate([15, 16, 17, 18, 19, 20, 21])
        ],
        [
            InlineKeyboardButton(z[3][day-22].split(".")[2], callback_data=dumps(dict(answer="none", day=int(z[3][day-22].split(".")[2]), month = int(z[3][day-22].split(".")[1]), text=text), ensure_ascii=False))
            for num, day in enumerate([22, 23, 24, 25, 26, 27, 28])
        ],
        [
            InlineKeyboardButton(z[4][day-29].split(".")[2], callback_data=dumps(dict(answer="none", day=int(z[4][day-29].split(".")[2]), month = int(z[4][day-29].split(".")[1]), text=text), ensure_ascii=False))
            for num, day in enumerate([29, 30, 31, 32, 33, 34, 35])
        ],
        [
            InlineKeyboardButton(" <<< ",
                                 callback_data=dumps((dict(answer="back", day=datetime.datetime.now().day, month=datetime.datetime.now().month)))),
            InlineKeyboardButton(calendry[month - 1],
                                 callback_data=dumps((dict(answer="none", day=datetime.datetime.now().day, month=datetime.datetime.now().month)))),
            InlineKeyboardButton(" >>> ",
                                 callback_data=dumps((dict(answer="forward", day=datetime.datetime.now().day, month=datetime.datetime.now().month))))
        ]
    ]
    await update.message.reply_text("Через сколько минут напомнить?", reply_markup=InlineKeyboardMarkup(keyboard))

async def delay(update: Update, day: int, month: int, text: str):
    number_even_numbers = 0
    time = datetime.datetime.now()
    for i in range(time.month, month):
        if i % 2 == 0:
            number_even_numbers += 1
    x = ((month - time.month)*30 + number_even_numbers) - time.day + day
    await update.callback_query.message.reply_text(f'Мы отправим сообщеньку через {x} секунд, то есть через количество дней до настоящей отправки')
    await asyncio.sleep(x)
    await update.callback_query.message.reply_text(text)


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    month = loads(update.callback_query.data)["month"]
    day = loads(update.callback_query.data)["day"]
    print(str(month) + ":" + str(day))
    if loads(update.callback_query.data)["answer"] == "back":
        if month-1 < datetime.datetime.now().month:
            await update.callback_query.message.reply_text("Невозможное действие")
        else:
            month -= 1
            await buttons(update, context, month)
            await update.callback_query.message.delete()
    elif loads(update.callback_query.data)["answer"] == "forward":
        if month >= 12:
            await update.callback_query.message.reply_text("Невозможное действие")
        else:
            month += 1
            await buttons(update, context, month)
            await update.callback_query.message.delete()
    else:
        if day < datetime.datetime.now().day and month == datetime.datetime.now().month or month < datetime.datetime.now().month:
            await update.callback_query.message.reply_text("Невозможное действие")
        else:
            await get_time(update, day, month, loads(update.callback_query.data)["text"])
            #asyncio.create_task(delay(update, day, month, loads(update.callback_query.data)["text"] ))










# todo: оформить выбор времени напоминания
# todo офрмить сохраиеие напоминаний при выключение и старата сервиса
# todo офрмить логирование запросов
# todo баг со временем(не правильно посчитал количество днеё до 29   июля, проблема с чётными месецами
