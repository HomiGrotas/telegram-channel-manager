import logging
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler

from bot.admin import help
from bot.admin.add_event import create_event_handler

from credentials import TOKEN


GROUP_ID = "beesIsrael"
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", help.start))
    application.add_handler(create_event_handler())

    application.run_polling()
