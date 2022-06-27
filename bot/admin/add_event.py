from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters

from enum import Enum

from bot.admin.security import managers_only


class Stages(Enum):
    DESCRIPTION = 1
    LOCATION = 2
    PHOTO = 3
    CONTACT = 4


def create_event_handler():
    add_event_handler = ConversationHandler(
        entry_points=[CommandHandler("event", start)],
        states={
            Stages.DESCRIPTION:  [MessageHandler(filters.TEXT, get_description)],
            Stages.LOCATION: [MessageHandler(filters.LOCATION | filters.TEXT, get_location)],
            Stages.PHOTO:  [MessageHandler(filters.PHOTO, get_picture)],
            Stages.CONTACT:  [MessageHandler(filters.TEXT | filters.CONTACT, get_contact_info)],
        },
        fallbacks=[]
    )
    return add_event_handler


@managers_only
async def start(update: Update, _):
    await update.message.reply_text("Please enter an event description:")
    return Stages.DESCRIPTION


async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    description = update.message.text
    context.user_data["description"] = description
    await update.message.reply_text("Please enter an event location:")
    print(context.user_data)
    return Stages.LOCATION


async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location'] = update.message.text or update.message.location
    await update.message.reply_text("Please attach a photo:")
    print(context.user_data)
    return Stages.PHOTO


async def get_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['photo'] = update.message.photo[-1]
    await update.message.reply_text("please send a phone number or contact")
    print(context.user_data)
    return Stages.CONTACT


async def get_contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contact'] = update.message.text or update.message.contact
    await update.message.reply_text("conv ended")
    print(context.user_data)
    return ConversationHandler.END
