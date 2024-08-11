import logging

from telegram import Update
from handlers.basic_bot_handlers import start_command, help_command

async def help_command_button_handler(update, context):
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
        await random_question(update, context, from_button=True)
    elif command == 'help':
        await help_command(fake_update, context)

    # Questions buttons handler
    elif command == 'correct':
        await query.message.reply_text('Correct! Congratulations!')
    elif command == 'incorrect':
        await query.message.reply_text('Incorrect! Better luck next time!')

    await query.answer()
