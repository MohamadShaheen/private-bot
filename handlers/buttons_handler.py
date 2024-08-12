import logging
from telegram import Update
from datetime import datetime
from handlers.basic_bot_handlers import start_command, help_command

answered_question_flag = False

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

    await query.answer()


async def questions_button_handler(update, context):
    global answered_question_flag

    query = update.callback_query

    # Make sure to not allow the user to answer the question more than one time
    if not answered_question_flag:
        await query.answer()
        return

    # Fetch relevant data for logging
    command = query.data
    username = query.from_user.name
    user_id = query.from_user.id
    question = query.message.text.split('\n')[0]
    category = query.message.text.split('\n')[1].split('-')[1].strip()
    difficulty = query.message.text.split('\n')[2].split('-')[1].strip()
    keyboard = query.message.reply_markup.inline_keyboard
    correct_answer = ''

    for row in keyboard:
        for button in row:
            if button.callback_data == 'correct':
                correct_answer = button.text
                break

    if command == 'correct':
        logging.info(f'Question - {question}. Category - {category}. Difficulty - {difficulty}. '
                     f'User {username} of id {user_id} correctly answered the question. '
                     f'Correct answer - {correct_answer}. Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text('Correct! Congratulations!')
    else:
        # In case of incorrect answer, fetch the answer that the user provided
        incorrect_answer = ''

        for row in keyboard:
            for button in row:
                if button.callback_data == command:
                    incorrect_answer = button.text
                    break

        logging.info(f'Question - {question}. Category - {category}. Difficulty - {difficulty}. '
                     f'User {username} of id {user_id} answered the question incorrectly. User answer - {incorrect_answer}. '
                     f'Correct answer - {correct_answer}. Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text('Incorrect! Better luck next time!')

    await query.answer()

    # Set the flag to false in order to prevent the user from answering the question more than one time
    answered_question_flag = False
