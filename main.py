from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler

from telegram.ext import (
     Application,
     CommandHandler,
     MessageHandler,
     filters,
     ConversationHandler,
     ContextTypes)
from reminder import startrem, rem, get_time

GET_RIMEND, GET_TIME = range(2)

async def cancel():
    print("end")

def main() -> None:
    # cfg = safe_load(open('config.yml').read())
    application = Application.builder().token('7763666090:AAERuItWsxaK5MvDPTKapMXPxyEnf8QY1vA').build()
    handler1 = ConversationHandler(
        entry_points=[CommandHandler('start', startrem)],
        states=
        {
            GET_RIMEND: [MessageHandler(filters.TEXT & ~filters.COMMAND, rem)],
            GET_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    application.add_handler(handler1)

    try:
        application.run_polling(handler1)
    finally:
        application.remove_handler(handler1)


if __name__ == "__main__":
    main()

