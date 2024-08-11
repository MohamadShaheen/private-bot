import os
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

server_url = os.getenv('SERVER_URL')

async def random_question(update: Update, context: CallbackContext, from_button=False) -> None:
    logging.info(f'\'/question random\' command was used - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')

    if not from_button:
        command = update.message.text.split()
        if len(command) == 2 and command[0] == '/question' and command[1] == 'random':
            try:
                question = requests.get(server_url + '/questions/random-question/').json()
                await update.message.reply_text(question)
            except Exception as e:
                logging.error(f'{e} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
    else:
        try:
            question = requests.get(server_url + '/questions/random-question/').json()
            await update.message.reply_text(question)
        except Exception as e:
            logging.error(f'{e} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
