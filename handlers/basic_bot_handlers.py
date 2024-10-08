import logging
from telegram import Update
from datetime import datetime
from telegram.ext import CallbackContext
from handlers.handlers_logs import naive_logs
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def start_command(update: Update, context: CallbackContext) -> None:
    naive_logs(update=update, command='start')
    await help_command(update=update, context=context)

async def help_command(update: Update, context: CallbackContext) -> None:
    naive_logs(update=update, command='help')

    keyboard = [
        [InlineKeyboardButton('start', callback_data='start')],
        [InlineKeyboardButton('categories', callback_data='categories')],
        [InlineKeyboardButton('random question', callback_data='random question')],
        [InlineKeyboardButton('filter question', callback_data='filter question')],
        [InlineKeyboardButton('help', callback_data='help')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Available Commands', reply_markup=reply_markup)
