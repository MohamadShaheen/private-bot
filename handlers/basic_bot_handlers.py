import logging
from telegram import Update
from datetime import datetime
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def start_command(update: Update, context: CallbackContext) -> None:
    logging.info(f'/start command was used - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    await update.message.reply_text(f'Hi. I\'m {context.bot.first_name}. How may I /help you today?')

async def help_command(update: Update, context: CallbackContext) -> None:
    logging.info(f'/help command was used - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')

    keyboard = [
        [InlineKeyboardButton("/start", callback_data='start')],
        [InlineKeyboardButton("/categories", callback_data='categories')],
        [InlineKeyboardButton("/question random", callback_data='random question')],
        [InlineKeyboardButton("/help", callback_data='help')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Available Commands', reply_markup=reply_markup)
