import os
import random
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from handlers import buttons_handler
from telegram.ext import CallbackContext
from handlers.handlers_logs import naive_logs
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

server_url = os.getenv('SERVER_URL')

async def random_question(update: Update, context: CallbackContext, from_button=False) -> None:
    naive_logs(update=update, command='question random')
    buttons_handler.answered_question_flag = True

    if not from_button:
        command = update.message.text.split()
        if not (len(command) == 2 and command[0] == '/question' and command[1] == 'random'):
            return

    try:
        question = requests.get(server_url + '/questions/random-question/').json()
        buttons = [InlineKeyboardButton(answer, callback_data=f'incorrect{i + 1}') for i, answer in enumerate(question['incorrect_answers'])]
        buttons.append(InlineKeyboardButton(question['correct_answer'], callback_data='correct'))
        random.shuffle(buttons)
        keyboard = [buttons[i:i + 1] for i in range(0, len(buttons), 1)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = (
            f'{question['question']}\n'
            f'Category - {question['category']}\n'
            f'Difficulty - {question['difficulty']}\n'
        )
        if from_button:
            await update.callback_query.message.reply_text(reply_text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(reply_text, reply_markup=reply_markup)
    except Exception as e:
        logging.error(f'{e} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')

async def filter_question(update: Update, context: CallbackContext, from_button=False) -> None:
    naive_logs(update=update, command='question filter')
