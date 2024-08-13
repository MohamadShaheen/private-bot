import os
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from telegram.ext import CallbackContext
from handlers.handlers_logs import naive_logs
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

server_url = os.getenv('SERVER_URL')

async def categories_fetch_command(update: Update, context: CallbackContext) -> None:
    naive_logs(update=update, command='categories')

    try:
        categories = requests.get(server_url + '/categories/').json()

        buttons = [InlineKeyboardButton(category, callback_data=category) for category in categories]
        buttons.append(InlineKeyboardButton('None', callback_data='None_category'))

        sizes = [5, 4, 3, 2, 1]

        for size in sizes:
            if len(categories) % size == 0:
                keyboard = [buttons[i:i + size] for i in range(0, len(buttons), size)]
                break

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Available Categories', reply_markup=reply_markup)
    except Exception as e:
        logging.error(f'{e} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
