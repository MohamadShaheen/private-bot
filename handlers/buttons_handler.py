import logging
from telegram import Update
from datetime import datetime
from handlers.basic_bot_handlers import start_command, help_command

answered_question_flag = False
chosen_type_flag = False
chosen_difficulty_flag = False
chosen_category_flag = False
just_show_categories_flag = False

async def help_command_button_handler(update, context):
    query = update.callback_query
    command = query.data

    fake_update = Update(update.update_id, message=query.message)

    if command == 'start':
        await start_command(fake_update, context)
    elif command == 'categories':
        from handlers.categories_handlers import categories_fetch_command
        global just_show_categories_flag
        just_show_categories_flag = True
        await categories_fetch_command(fake_update, context)
    elif command == 'random question':
        from handlers.questions_handlers import random_question
        await random_question(fake_update, context)
    elif command == 'filter question':
        from handlers.questions_handlers import filter_question
        await filter_question(fake_update, context)
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

async def type_button_handler(update, context):
    global chosen_type_flag
    query = update.callback_query

    if not chosen_type_flag:
        await query.answer()
        return

    command = query.data
    username = query.from_user.name
    user_id = query.from_user.id

    if command == 'boolean':
        logging.info(f'User {username} of id {user_id} chose {command} question. '
                     f'Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text(f'Chosen type: {command}')
    elif command == 'multiple':
        logging.info(f'User {username} of id {user_id} chose multiple choice question. '
                     f'Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text(f'Chosen type: multiple choice')
    elif command == 'None_type':
        logging.info(f'User {username} of id {user_id} did not require specific type. '
                     f'Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text(f'Chosen type: None')
        command = None

    context.user_data['chosen_type'] = command
    chosen_type_flag = False

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    difficulty_buttons = [
        InlineKeyboardButton('easy', callback_data='easy'),
        InlineKeyboardButton('medium', callback_data='medium'),
        InlineKeyboardButton('hard', callback_data='hard'),
        InlineKeyboardButton('None', callback_data='None_difficulty'),
    ]
    keyboard = [difficulty_buttons[i:i + 2] for i in range(0, len(difficulty_buttons), 2)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('Choose Difficulty', reply_markup=reply_markup)
    await query.answer()

async def difficulty_button_handler(update, context):
    global chosen_difficulty_flag
    query = update.callback_query

    if not chosen_difficulty_flag:
        await query.answer()
        return

    command = query.data
    username = query.from_user.name
    user_id = query.from_user.id

    if command == 'easy':
        logging.info(f'User {username} of id {user_id} chose an {command} question. '
                     f'Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text(f'Chosen difficulty: {command}')
    elif command == 'medium' or command == 'hard':
        logging.info(f'User {username} of id {user_id} chose a {command} question. '
                     f'Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text(f'Chosen difficulty: {command}')
    elif command == 'None_difficulty':
        logging.info(f'User {username} of id {user_id} did not require a specific difficulty. '
                     f'Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text(f'Chosen difficulty: None')
        command = None

    context.user_data['chosen_difficulty'] = command
    chosen_difficulty_flag = False
    await query.answer()

    from handlers.categories_handlers import categories_fetch_command
    await categories_fetch_command(update=Update(update.update_id, message=query.message), context=context)

async def categories_button_handler(update, context):
    # If just the categories are requested reject the function
    global just_show_categories_flag
    global chosen_category_flag
    query = update.callback_query
    if just_show_categories_flag:
        await query.answer()
        just_show_categories_flag = False
        chosen_category_flag = False
        return

    if not chosen_category_flag:
        await query.answer()
        return

    command = query.data
    username = query.from_user.name
    user_id = query.from_user.id

    if command == 'None_category':
        logging.info(f'User {username} of id {user_id} did not request a specific category. '
                     f'Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text(f'Chosen category: None')
        command = None
    else:
        logging.info(f'User {username} of id {user_id} requested a question about {command}. '
                     f'Time - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        await query.message.reply_text(f'Chosen category: {command}')

    context.user_data['chosen_category'] = command
    chosen_category_flag = False
    await query.answer()

    data = {
        'type': context.user_data['chosen_type'],
        'difficulty': context.user_data['chosen_difficulty'],
        'category': context.user_data['chosen_category']
    }

    import requests
    from handlers.questions_handlers import server_url, show_question
    import random
    try:
        questions = requests.get(f'{server_url}/questions/filter/', data=data).json()['questions']
        question = random.choice(questions)
        await show_question(update=Update(update.update_id, message=query.message), context=context, question=question)
    except Exception as e:
        logging.error(f'{e} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')

    # Make sure to allow  the user to get the categories after finishing
    context.user_data['blocked'] = False
