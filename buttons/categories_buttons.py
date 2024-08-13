import random
import logging
from telegram import Update
from datetime import datetime
from handlers.questions_handlers import server_url, show_question
from utils.requests_from_server import request_get_endpoint_from_server


async def categories_button_handler(update, context):
    # If just the categories are requested reject the function
    query = update.callback_query

    if 'just_show_categories' in context.user_data:
        if context.user_data['just_show_categories']:
            await query.answer()
            context.user_data['just_show_categories'] = False
            return

    if not context.user_data['chosen_category_flag']:
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
    context.user_data['chosen_category_flag'] = False
    await query.answer()

    params = {
        'type': context.user_data['chosen_type'],
        'difficulty': context.user_data['chosen_difficulty'],
        'category': context.user_data['chosen_category']
    }

    try:
        questions = await request_get_endpoint_from_server(url=f'{server_url}/questions/filter/', params=params)
        questions = questions['questions']
        # questions = requests.get(f'{server_url}/questions/filter/', params=params).json()['questions']
        question = random.choice(questions)
        await show_question(update=Update(update.update_id, message=query.message), context=context, question=question)
    except Exception as e:
        logging.error(f'{e} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
