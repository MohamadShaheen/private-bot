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


async def button_handler(update, context):
    query = update.callback_query
    command = query.data

    fake_update = Update(update.update_id, message=query.message)

    if command == 'start':
        await start_command(fake_update, context)
    elif command == 'categories':
        from handlers.categories_handlers import categories_fetch_command
        await categories_fetch_command(fake_update, context)
    elif command == 'random question':
        from handlers.questions_handlers import random_question
        await random_question(fake_update, context, from_button=True)
    elif command == 'help':
        await help_command(fake_update, context)

    await query.answer()
