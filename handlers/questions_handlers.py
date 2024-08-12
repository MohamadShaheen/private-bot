import os
import random
import asyncio
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

async def show_question(update: Update, context: CallbackContext, question) -> None:
    buttons = [InlineKeyboardButton(answer, callback_data=f'incorrect{i + 1}') for i, answer in
               enumerate(question['incorrect_answers'])]
    buttons.append(InlineKeyboardButton(question['correct_answer'], callback_data='correct'))
    random.shuffle(buttons)
    keyboard = [buttons[i:i + 1] for i in range(0, len(buttons), 1)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_text = (
        f'{question['question']}\n'
        f'Category - {question['category']}\n'
        f'Difficulty - {question['difficulty']}\n'
    )
    await update.message.reply_text(reply_text, reply_markup=reply_markup)

async def random_question(update: Update, context: CallbackContext) -> None:
    naive_logs(update=update, command='question_random')
    buttons_handler.answered_question_flag = True

    try:
        question = requests.get(server_url + '/questions/random-question/').json()
        await show_question(update=update, context=context, question=question)
    except Exception as e:
        logging.error(f'{e} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')

async def filter_question(update: Update, context: CallbackContext) -> None:
    # Make sure to prevent the user from intervening while getting the question
    context.user_data['blocked'] = True

    naive_logs(update=update, command='question_filter')
    buttons_handler.chosen_type_flag = True
    buttons_handler.chosen_difficulty_flag = True
    buttons_handler.answered_question_flag = True

    type_buttons = [
        InlineKeyboardButton('boolean', callback_data='boolean'),
        InlineKeyboardButton('multiple choice', callback_data='multiple'),
        InlineKeyboardButton('None', callback_data='None_type')
    ]
    keyboard = [type_buttons[i:i + 2] for i in range(0, len(type_buttons), 2)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose Type', reply_markup=reply_markup)
