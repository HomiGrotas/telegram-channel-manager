from telegram import Update
from telegram.ext import ContextTypes

from utils.parser import parser

managers = [int(user_id) for user_id in parser.get('bot', 'managersID')[1:-1].split(',')]


def managers_only(func):
    """
    only managers are allowed to use functions which
    calls this decorator
    :param func: function to protect
    """
    async def restricted_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in managers:
            print(update.effective_user.id)
            await update.message.reply_text("No permission to use this function")
        else:
            return await func(update, context)
    return restricted_function
