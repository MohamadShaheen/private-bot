import logging
from telegram import Update
from datetime import datetime
from telegram.ext import CallbackContext

async def start_command(update: Update, context: CallbackContext) -> None:
    logging.info(f'/start command was used - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    await update.message.reply_text(f'Hi. I\'m {context.bot.first_name}. How may I /help you today?')

async def help_command(update: Update, context: CallbackContext) -> None:
    logging.info(f'/help command was used - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')

    help_commands = (
        '/start - Start the bot\n'
        '/categories - Get all the available categories\n'
        '/help - Show the bot available commands'
    )

    await update.message.reply_text(help_commands)
