from telegram.ext import CallbackQueryHandler

from yaml import safe_load

from telegram.ext import Application, MessageHandler, filters, ContextTypes
from reminder import  rem, handle_button

GET_RIMEND, GET_TIME = range(2)

async def cancel():
    print("end")

def main() -> None:
    cfg = safe_load(open('config.yml').read())
    application = Application.builder().token(cfg['token']).build()

    handler = MessageHandler(filters=filters.TEXT, callback=rem)
    btn_handler = CallbackQueryHandler(handle_button)
    try:
        application.add_handler(handler)
        application.add_handler(btn_handler)
        application.run_polling(1)
    finally:
        application.remove_handler(handler)
        application.remove_handler(btn_handler)


if __name__ == "__main__":
    main()

